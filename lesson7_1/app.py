import streamlit as st
import pandas as pd
import time
from crawl4ai import Crawler

# 匯率資料快取
@st.cache_data(ttl=600)
def get_rates():
    # 這裡以假資料模擬，請根據 crawl4ai 實作
    # crawler = Crawler()
    # rates = crawler.get_rates()
    rates = pd.DataFrame({
        '貨幣': ['USD', 'JPY', 'EUR', 'CNY', 'KRW', 'VND', 'IDR', 'THB', 'MYR', 'SGD'],
        '匯率': [32.1, 0.22, 35.5, 4.5, 0.025, 0.0013, 0.0021, 0.92, 6.8, 23.5],
        '可交易': [True, True, True, True, False, True, False, True, True, True]
    })
    return rates

def main():
    st.set_page_config(page_title="台幣匯率轉換", layout="wide")
    st.title("台幣匯率轉換工具")
    rates = get_rates()
    # 過濾可交易貨幣
    tradable = rates[rates['可交易']]
    col1, col2 = st.columns(2)
    with col1:
        st.header("台幣轉換")
        currency = st.selectbox("選擇貨幣", tradable['貨幣'])
        amount = st.number_input("請輸入台幣金額", min_value=0.0, value=1000.0)
        rate = tradable[tradable['貨幣'] == currency]['匯率'].values[0]
        st.write(f"{amount} TWD = {amount / rate:.2f} {currency}")
        if st.button("手動更新匯率"):
            st.cache_data.clear()
            st.experimental_rerun()
    with col2:
        st.header("匯率表格")
        df = tradable[['貨幣', '匯率']].copy()
        df['匯率'] = df['匯率'].apply(lambda x: x if pd.notnull(x) else '暫停交易')
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
