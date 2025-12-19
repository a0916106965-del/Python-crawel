import json
from datetime import datetime
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

@st.cache_data(ttl=600)  # 10分鐘快取
def fetch_exchange_rates():
    """使用 requests + BeautifulSoup 爬取匯率（無 asyncio 問題）"""
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 找到匯率表格
        table = soup.find('table', {'title': '牌告匯率'})
        if not table:
            return pd.DataFrame()
        
        rows = table.find_all('tr')[1:]  # 跳過標題列
        data = []
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                currency = cells[0].get_text(strip=True)
                buy_rate = cells[1].get_text(strip=True)
                sell_rate = cells[2].get_text(strip=True)
                
                data.append({
                    '幣別': currency,
                    '本行即期買入': buy_rate if buy_rate else '暫停交易',
                    '本行即期賣出': sell_rate if sell_rate else '暫停交易'
                })
        
        df = pd.DataFrame(data)
        
        # 處理空值
        df['本行即期買入'] = df['本行即期買入'].replace('', '暫停交易').fillna('暫停交易')
        df['本行即期賣出'] = df['本行即期賣出'].replace('', '暫停交易').fillna('暫停交易')
        
        # 過濾無法交易貨幣
        df = df[~((df['本行即期買入'] == '暫停交易') & (df['本行即期賣出'] == '暫停交易'))]
        
        return df
        
    except Exception as e:
        st.error(f"網路請求失敗：{str(e)}")
        return pd.DataFrame()

def main():
    st.set_page_config(
        page_title="台幣匯率轉換",
        page_icon="💱",
        layout="wide"
    )
    
    st.title("💱 台幣匯率轉換系統")
    st.markdown("---")
    
    # 手動更新按鈕
    col_update = st.columns([6, 1])[1]
    with col_update:
        if st.button("🔄 手動更新", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    st.info(f"📅 最後更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        with st.spinner("正在取得最新匯率資料..."):
            df = fetch_exchange_rates()
        
        if df.empty:
            st.error("❌ 無法取得匯率資料，請檢查網路連線")
            return
        
        st.success(f"✅ 成功取得 {len(df)} 種貨幣匯率")
        
        # 雙欄布局
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 台灣銀行牌告匯率")
            st.dataframe(
                df, use_container_width=True, hide_index=True, height=600
            )
        
        with col2:
            st.subheader("💰 台幣轉換計算器")
            
            # 可交易貨幣
            tradable_df = df[
                (df['本行即期買入'] != '暫停交易') | 
                (df['本行即期賣出'] != '暫停交易')
            ].copy()
            
            if tradable_df.empty:
                st.warning("⚠️ 目前沒有可交易的貨幣")
                return
            
            # 輸入與選擇
            twd_amount = st.number_input(
                "輸入台幣金額 (TWD)", min_value=0.0, value=10000.0, 
                step=100.0, format="%.2f"
            )
            
            currency_list = tradable_df['幣別'].tolist()
            selected_currency = st.selectbox("選擇目標貨幣", currency_list)
            
            if selected_currency:
                row = tradable_df[tradable_df['幣別'] == selected_currency].iloc[0]
                
                st.markdown(f"### 📈 {selected_currency} 匯率")
                col_buy, col_sell = st.columns(2)
                
                with col_buy:
                    st.metric("本行買入", row['本行即期買入'])
                with col_sell:
                    st.metric("本行賣出", row['本行即期賣出'])
                
                st.markdown("### 💵 轉換結果")
                
                sell_rate = row['本行即期賣出']
                if sell_rate != '暫停交易':
                    try:
                        rate = float(re.sub(r'[^\d.]', '', sell_rate))
                        foreign = twd_amount / rate
                        
                        st.success(
                            f"**{twd_amount:,.2f} TWD** = **{foreign:,.4f} {selected_currency}**"
                        )
                        st.caption(f"匯率：{rate:.4f} (本行賣出)")
                    except:
                        st.error("匯率格式錯誤")
                else:
                    st.warning("⚠️ 此貨幣暫停交易")
    
    except Exception as e:
        st.error(f"❌ 錯誤：{str(e)}")

if __name__ == "__main__":
    main()
