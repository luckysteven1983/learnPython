'''
Created on Dec 9, 2015

@author: dadl
'''
import os
class GetFileList(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def getFileList(self, lab, localdir):
        '''
        get files from local directory       
        '''      
        #cmd = "ls "+dir+" | grep ^top | grep log$ | grep D | grep -v parsed"
        cmd = "ls "+localdir+" | grep ^top | grep log$ | grep -v parsed"
        #result = os.popen(cmd).read()
        k = []
        for i in os.popen(cmd).readlines():
            j = i.strip()
            k.append(j)
        return k        