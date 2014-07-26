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
while j < len(neg)
    if neg(i) < neg(j):
        minus = j - i

