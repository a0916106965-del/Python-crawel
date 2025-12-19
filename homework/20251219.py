import asyncio
import json
from datetime import datetime

import streamlit as st
import pandas as pd

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


# =========================
# 取得匯率資料（含快取）
# =========================
@st.cache_data(ttl=600)  # 10 分鐘快取
def fetch_exchange_rates():
    """爬取台灣銀行匯率資料（同步包裝非同步）"""

    async def _fetch():
        schema = {
            "name": "匯率資訊",
            "baseSelector": "table[title='牌告匯率'] tr",
            "fields": [
                {
                    "name": "幣別",
                    "selector": "td[data-table='幣別'] div.print_show",
                    "type": "text",
                },
                {
                    "name": "本行即期買入",
                    "selector": "td[data-table='本行即期買入']",
                    "type": "text",
                },
                {
                    "name": "本行即期賣出",
                    "selector": "td[data-table='本行即期賣出']",
                    "type": "text",
                },
            ],
        }

        strategy = JsonCssExtractionStrategy(schema)

        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=strategy,
        )

        async with AsyncWebCrawler() as crawler:
            url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
            result = await crawler.arun(url=url, config=run_config)
            return json.loads(result.extracted_content)

    # 🔑 Streamlit 正確執行 async 的方式
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(_fetch())
    loop.close()

    df = pd.DataFrame(data)

    if not df.empty:
        df["本行即期買入"] = (
            df["本行即期買入"].replace("", "暫停交易").fillna("暫停交易")
        )
        df["本行即期賣出"] = (
            df["本行即期賣出"].replace("", "暫停交易").fillna("暫停交易")
        )

        # 移除完全無法交易的幣別
        df = df[
            ~(
                (df["本行即期買入"] == "暫停交易")
                & (df["本行即期賣出"] == "暫停交易")
            )
        ]

    return df


# =========================
# Streamlit 主程式
# =========================
def main():
    st.set_page_config(
        page_title="台幣匯率轉換",
        page_icon="💱",
        layout="wide",
    )

    st.title("💱 台幣匯率轉換系統")
    st.markdown("---")

    # 手動更新
    col_update = st.columns([6, 1])[1]
    with col_update:
        if st.button("🔄 手動更新", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    st.info(f"📅 最後更新時間：{datetime.now():%Y-%m-%d %H:%M:%S}")

    try:
        df = fetch_exchange_rates()

        if df.empty:
            st.error("❌ 無法取得匯率資料")
            return

        col1, col2 = st.columns(2)

        # ===== 左側：匯率表 =====
        with col1:
            st.subheader("📊 台灣銀行牌告匯率")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=600,
            )

        # ===== 右側：轉換器 =====
        with col2:
            st.subheader("💰 台幣轉換計算器")

            tradable_df = df[
                (df["本行即期買入"] != "暫停交易")
                | (df["本行即期賣出"] != "暫停交易")
            ]

            if tradable_df.empty:
                st.warning("⚠️ 目前沒有可交易的貨幣")
                return

            twd_amount = st.number_input(
                "輸入台幣金額 (TWD)",
                min_value=0.0,
                value=10000.0,
                step=100.0,
                format="%.2f",
            )

            currency = st.selectbox(
                "選擇目標貨幣",
                tradable_df["幣別"].tolist(),
            )

            row = tradable_df[tradable_df["幣別"] == currency].iloc[0]

            buy_rate = row["本行即期買入"]
            sell_rate = row["本行即期賣出"]

            st.markdown("---")
            st.metric("本行買入", buy_rate)
            st.metric("本行賣出", sell_rate)

            st.markdown("---")
            st.subheader("💵 轉換結果")

            if sell_rate != "暫停交易":
                try:
                    rate = float(sell_rate)
                    foreign_amount = twd_amount / rate
                    st.success(
                        f"{twd_amount:,.2f} TWD = {foreign_amount:,.4f} {currency}"
                    )
                    st.caption(f"使用匯率：{rate:.4f}（本行賣出）")
                except ValueError:
                    st.error("❌ 匯率格式錯誤")
            else:
                st.warning("⚠️ 此貨幣暫停交易")

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")


if __name__ == "__main__":
    main()
