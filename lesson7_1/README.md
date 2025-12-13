# 台幣匯率轉換專案

## 專案說明
- 使用 crawl4ai 爬取匯率資料
- 使用 streamlit 製作前端介面，分為兩欄：
  - 左欄：台幣轉換計算
  - 右欄：表格顯示匯率資料，並可輸入金額
- 每 10 分鐘自動更新，並可手動更新
- 欄位若為空顯示「暫停交易」
- 無法交易的貨幣不顯示

## 執行方式
1. 安裝依賴：`uv pip install -r requirements.txt`
2. 啟動服務：`streamlit run app.py`
