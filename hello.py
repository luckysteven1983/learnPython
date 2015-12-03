# -*- coding: utf-8 -*-
print 'Hello World!'
#name = raw_input('Please enter your name: ')
#print 'hello',name
#sum = 0
#n = 1
#while n < 100:
#    sum = sum + n
#    n = n + 2
#print sum

#age = 3
#if age >= 18:
#    print 'adult'
#elif age >= 6:
#    print 'teenager'
#else:
#    print 'kid'

names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print name

a = 0 #"NameError: name 'a' is not defined" if a is not defined like this
for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    a = a + x
print a

sum = 0
for x in range(101):
    sum = sum + x
print sum

#birth = int(raw_input('birth: '))
#print 'birth: ',birth
#if birth < 2000:
#    print u'00前'
#else:
#    print u'00后'

#input = int(raw_input('Please input a value: '))
def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x
#print my_abs(input)