# 定義類別、與類別屬性(封裝在類別中的變數與函式)
# 定義一個類別IO,有2個屬性 supportedsrcs與 read
#IO=imput與output的縮寫
#console=終端機

class IO:
    supportedsrcs=["console","file"]
    def read(src):
        if src not in IO.supportedsrcs:
            print("Not supported")
      
        else:
            print("Read file",src)

#使用類別
print(IO.supportedsrcs)
IO.read("file")
IO.read("internet")



