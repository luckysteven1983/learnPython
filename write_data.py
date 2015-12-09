#!/usr/bin/env python
# -*- coding: cp936 -*-
read_f = open('test.log','r')
f = open('tmp.log','w')
for l in read_f:
    ll = l.split(' ')

    f.writelines("0,0,%s,0,%s,%s,0,0,0\n" %(ll[0],ll[1],ll[3].strip('\n')))
f.close()
read_f.close()
