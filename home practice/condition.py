n1=int(input("請輸入數字一:"))
n2=int(input("請輸入數字二:"))
op=input("請輸入運算符號(+,-,*,/):")
if op=='+':
    print(n1+n2)
elif op=='-':
    print(n1-n2)
elif op=='*':
    print(n1*n2)
elif op=='/':
    print(n1/n2) 
else:
    print("不支援此運算符號")
