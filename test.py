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

def binarySearch(lists,select):
    is_none=False
    if lists != []:
        cen_num=len(lists)/2
        tlag=lists[cen_num]
        gt_list=lists[0:cen_num]
        lt_list=lists[cen_num+1:]
 
    if tlag==select:
is_none=True
returnis_none
eliftlag>select:
is_se=binarySearch(gt_list,select)
ifnotis_se:
returnbinarySearch(lt_list,select)
returnis_none
eliftlag<select:
is_se=binarySearch(lt_list,select)
ifnotis_se:
returnbinarySearch(gt_list,select)
returnis_none
