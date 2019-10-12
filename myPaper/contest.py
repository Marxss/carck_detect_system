# n=int(input())
# a,b=list(map(int,input().strip().split()))

string=input()
dic={}
for i in string:
    if i in dic.keys():
        dic[i]+=1
    else:
        dic[i]=1
#print(dic)
strings=sorted(dic.items(),key=lambda x:x[1],reverse=True)
#print(strings)
lenght=len(strings)
res=0
if lenght<3:
    for item in strings:
        res+=item[1]
elif lenght<7:
    b=[2,2,2,3,4]
    for i,item in enumerate(strings):
        res+=item[1]*b[i]
print(res)










