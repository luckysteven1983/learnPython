a = [-1, -2, -10, 0, 0, 4, 5, 9]
print a
neg = []
zero = []
pos = []
while a:
    num = a.pop()
    if num < 0:
        neg.append(num)
    if num == 0:
        zero.append(num)
    if num > 0:
        pos.append(num)
zero.extend(pos)
neg.extend(zero)
print neg
neg.sort()
print neg
neg.reverse()
print neg
i = 0
j = 1
minus = 0
max = 0
maxi = 0
maxj = 0
b = [-1, -2, -10, 0, 0, 4, 5, 9]
#print len(b)
print b
while i < len(b):
    #Don't forget to reset j, or the loop will not do again since j is bigger than leng(b) after below loop done.
    j = i + 1
    while j < len(b):
        if b[i] < b[j]:
            minus = j - i
            if max < minus:
	        max = minus
                maxi = i
                maxj = j
        j = j + 1 
	#print i,j-1,max
    i = i + 1
print b[maxi],b[maxj]

import sys  
  
def search2(a,m):  
    low = 0  
    high = len(a) - 1  
    while low<=high:  
        mid = (low + high)/2  
        midval = a[mid]  
  
        if midval<m:  
            low = mid + 1  
        elif midval>m:  
            high = mid-1  
        else:  
            print mid  
            return mid  
    print -1  
    return -1  
  
if __name__ == "__main__":  
  
    a = [int(i) for i in list(sys.argv[1])]  
    m = int(sys.argv[2])  
    search2(a,m)  

def bubble(bubbleList):
    listLength=len(bubbleList)
    j = 0
    while j < listLength:
        for i in range(listLength - 1):
            #print i
            if bubbleList[i] > bubbleList[i+1]:
                #temp = bubbleList[i]
                #bubbleList[i] = bubbleList[i+1]
                #bubbleList[i+1] = temp
		bubbleList[i],bubbleList[i+1]=bubbleList[i+1],bubbleList[i]
                #listLength = listLength - 1
                #print i
                #print listLength
                #print bubbleList
        j = j + 1
	#print bubbleList
    print bubbleList
if __name__=='__main__':
    bubbleList=[3,4,1,2,5,8,0]
    bubble(bubbleList)


def bubbletest(List):
    for n in range(len(List)-1,0,-1):
        for m in range(0,n):
            if List[m]>List[m+1]:List[m],List[m+1]=List[m+1],List[m]
    return List
if __name__=='__main__':
    mylist = [3,4,1,2,5,8,0]
    bubbletest(mylist)
    #print mylist
