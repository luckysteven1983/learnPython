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
        myFile = open(fileInput, "r")
        cpuData = myFile.readlines()
        lineNum = 0
        for line in cpuData:
	    line = line.strip()
            lineNum += 1
            found = re.search(r'top - (\d\d:\d\d:\d\d).', line)
            if found:
                timeIndex = found.group(1)
                if self.timeCompare(startTime, timeIndex):
                    break
                else:
                    continue
        currentLineNum = lineNum
        for line in cpuData[currentLineNum:-1]:
	    line = line.strip()
            found = re.search(r'top - (\d\d:\d\d:\d\d).', line)
            if found:
                timeIndex = found.group(1)
                if self.timeCompare(endTime, timeIndex):
                    break
                else:
                    continue
            print line

            found = re.search('PDLSI', line)
            if found:
                key = line.split()[11]
                cpu = line.split()[8]
                dictCpu[key].append(cpu)

        myFile.close()
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
	cmd = "ls "+dir+" | grep test.txt"
	result = os.popen(cmd).read()
        output = result.strip().split(os.linesep)
        return output

    def cptAnaAll(self, startTime, endTime, lab, dir):
        '''
        '''
        dict={}
        for fileIndex in self.getFileList(lab, dir):
            fileIndex = dir+'/'+fileIndex
            result = self.cpuAna(startTime, endTime, fileIndex)
            bladeNumber = 1
            dict[bladeNumber] = result
        return dict
    
    def anaAll(self, dict):
        pass

cpuAnaAManager =  CPUAnaAManager()
dict1 = cpuAnaAManager.cptAnaAll('16:43:42', '16:43:44', 'atca47', './rawdata')
cpuAnaAManager.anaAll(dict1)




