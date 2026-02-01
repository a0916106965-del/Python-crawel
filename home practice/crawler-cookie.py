#抓取PTT八卦版的網頁原始碼(HTML)
import urllib.request as req
url="https://www.ptt.cc/bbs/Gossiping/index.html"
#建立一個Request物件，附加Request Headers的資訊
#利用request物件去開啟網址(送出Request)，並取得回應資料
#user-agent:告訴伺服器我們是用什麼裝置、瀏覽器在看網頁
request=req.Request(url,headers={
    "cookie":"over18=1",
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36 Edg/144.0.0.0"
})
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
print(data)

#解析原始碼，取得每篇文章的標題
#利用BeautifulSoup協助我們解析HTML格式文件
import bs4
root=bs4.BeautifulSoup(data,"html.parser")
#尋找所有class="title"的div標籤
#root代表整份HTML文件
#string:取得標籤內的文字內容
titles=root.find_all("div",class_="title") 
for title in titles:
    if title.a != None: #如果標題包含a標籤(沒有被刪除).印出來
        print(title.a.string) #印出標題內容

