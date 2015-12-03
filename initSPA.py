#!/usr/bin/python
import os
import time

loopTime = int(raw_input("Please enter loop NUMBER(1~5):"))
if loopTime > 5:
    print "Loop NUMBER should be 1 to 5, thanks!"
    exit(0) 
while loopTime > 0:
    os.system("echo \"########################################\"")
    print "Loop "+str(loopTime)+" time starts at "+time.ctime()+"."
    os.system("echo \"########################################\"")
    print "Remove SPA starts at "+time.ctime()+"."
    os.system("/sn/cr/cepexec RMV_SPA rmv:spa=OAM422")
    print "Remove SPA completes at "+time.ctime()+"."
    time.sleep(2)
    print "Delete SPA starts at "+time.ctime()+"."
    os.system("/sn/cr/cepexec DELETE_SPA delete:spa=OAM422,proc")
    print "Delete SPA completes at "+time.ctime()+"."
    time.sleep(2)
    print "Install SPA starts at "+time.ctime()+"."
    os.system("/sn/cr/cepexec INSTALL_SPA install:spa=OAM422,proc")
    print "Install SPA completes at "+time.ctime()+"."
    time.sleep(2)
    print "Restart SPA starts at "+time.ctime()+"."
    os.system("/sn/cr/cepexec RST_SPA rst:spa=OAM422")
    print "Restart SPA completes at "+time.ctime()+"."
    os.system("echo \"########################################\"")
    print "Loop "+str(loopTime)+" time completes at "+time.ctime()+"."
    os.system("echo \"########################################\"")	
    time.sleep(5)
    loopTime -= 1
