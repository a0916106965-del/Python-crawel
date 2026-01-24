#實體物件的建立與使用_上篇
#Point 實體物件的設計:平面座標上的點
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
#建立第一個實體物件
p1=Point(3,4)
print(p1.x,p1.y)
#建立第二個實體物件
p2=Point(5,6)
print(p2.x,p2.y)

#FullName 實體物件的設計: 分開紀錄姓與名,並組合成全名(一)
class FullName:
    def __init__(self):
        self.first="show"
        self.last="hu"
name1=FullName()
print(name1.first,name1.last)

#FullName 實體物件的設計: 分開紀錄姓與名,並組合成全名(二)
class FullName:
    def __init__(self,first,last):
        self.first=first
        self.last=last
name1=FullName("show","hu")
print(name1.first,name1.last)
name2=FullName("kitty","hello")
print(name2.first,name2.last)