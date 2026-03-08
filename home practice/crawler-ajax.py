#抓取 medium.com 的文章資料
import urllib.request as req
url="https://medium.com/_/graphql"
#建立一個Request物件，附加Request Headers的資訊
#利用request物件去開啟網址(送出Request)，並取得回應資料
#user-agent:告訴伺服器我們是用什麼裝置、瀏覽器在看網頁
request=req.Request(url,headers={
       "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36 Edg/144.0.0.0"
})
with req.urlopen(request) as response:
    data=response.read().decode("utf-8") #根據觀察,取得的資料是JSON格式的字串,所以不需要再用BeautifulSoup解析了

#解析 json 格式的資料，取得每篇文章的標題
import json
data=data.replace("])}while(1);</x>","") #把前面多餘的字串去掉,留下真正的json資料
#data=json.loads(data) #把原始的json資料解析成字典/列表的表示形式
print(data)
