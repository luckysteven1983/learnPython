'''
Created on Nov 4, 2015

@author: xzhao015
'''
import re
import os
class CPUAnaAManager(object):
    '''
    classdocs
    
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def timeCompare(self, time1, time2):
        '''
        18:03:03
        true is >
        '''
        if cmp(time1, time2) <= 0:
            return True
        else:
            return False

    def cpuAna(self, startTime, endTime, fileInput):
        '''
        '''
        dictCpu={}
        dictCpu['PDLSI1']=[]
        dictCpu['PDLSI2']=[]
        dictCpu['PDLSI3']=[]
        print fileInput
        myFile = open(fileInput, "r")
        cpuData = myFile.readlines()
        for line in cpuData:
            found = re.search(r'top - (\d\d:\d\d:\d\d).', line)
            if found:
                timeIndex = found.group(1)
                if self.timeCompare(startTime, timeIndex):
                    continue
                if self.timeCompare(timeIndex, endTime):
                    break
            found = re.search('PDLSI', line)
            if found:
                key = line.split()[11]
                cpu = line.split()[8]
                dictCpu[key].append(cpu)
        return dictCpu

    def getFileList(self, lab, dir):
        '''
        get files from lab
        '''
        #cmd = "mdkir -f tmp4CPU"
        #os.popen(cmd)
        #cmd = "scp "+dir+"top* tmp4CPU"
        #os.popen(cmd)
        
        fileList = ""
        #cmd = "ls "+dir+"/top_L_16:43:40.log | grep ^top | grep log$"
        cmd = "ls "+dir+" | grep ^top | grep log$ | grep L"
        result = os.popen(cmd).readlines()
        #fileList = result.split()
        for index in result:
            fileList += index
        output = fileList.split(os.linesep)
        return output

    def cptAnaAll(self, startTime, endTime, lab, dir):
        '''
        '''
        dict={}
        self.getFileList(lab, dir)
        for fileIndex in self.getFileList(lab, dir):
            fileIndex = dir+'/'+fileIndex
            print fileIndex
            while len(fileIndex) != 0:
                result = self.cpuAna(startTime, endTime, fileIndex)
            bladeNumber = 1
            dict[bladeNumber] = result
        return dict
    
    def anaAll(self, dict):
        print

cpuAnaAManager =  CPUAnaAManager()
dict1 = cpuAnaAManager.cptAnaAll('16:45:00', '16:45:20', 'atca47', './rawdata')
cpuAnaAManager.anaAll(dict1)




