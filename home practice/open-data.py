#網路連線
import urllib .request as request
str="https://www.ntu.edu.tw/"
with request.urlopen(str) as response:
    data=response.read() #取得台灣大學網站的原始碼(HTML.CSS.JSON)
print(data)
#串接.擷取公開資料



