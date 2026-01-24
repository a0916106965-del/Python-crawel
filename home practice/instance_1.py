#實體物件的建立與使用_下篇
#Point 實體物件的設計:平面座標上的點
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    #定義實體方法
    def show(self):
        print(self.x,self.y)
    def distance(self,targetx,targety):
        return(((self.x-targetx)**2)+(self.y-targety)**2)**0.5
p=Point(3,4)
p.show() #呼叫實體方法/函式
result=p.distance(0,0) #計算座標(3,4)和座標(0,0)的距離
print("距離:",result)


#FullName 實體物件的設計: 包裝檔案讀取的程式
#自己註解:利用類別建立實體物件
class File:
    #初始化函式,建立2個實體屬性:name與file
    def __init__(self,name):
        self.name=name
        self.file=None #尚未開啟檔案:初期是None
    #實體方法:open與read
    def open(self):
        self.file=open(self.name,"r",encoding="utf-8")
    def read(self):
        return self.file.read()
#讀取第一個檔案
f1=File("data1.txt")
f1.open()
data=f1.read()
print(data)

#讀取第二個檔案
f2=File("data2.txt")
f2.open()
data=f2.read()
print(data)