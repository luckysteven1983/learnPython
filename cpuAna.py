'''
Created on Nov 4, 2015

@author: xzhao015
'''
import re
import os
import csv
class CPUAnaAManager(object):
    '''
    classdocs
    
    '''
    dictCpu = {}

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
        dictCpu = {}
        #dictCpu['PDLSI1']=[]
        #dictCpu['PDLSI2']=[]
        #dictCpu['PDLSI3']=[]
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
        currentLineNum = lineNum - 1
        for line in cpuData[currentLineNum:-1]:
            line = line.strip()
            found = re.search(r'top - (\d\d:\d\d:\d\d).', line)
            if found:
                timeIndex = found.group(1)
                dictKey = timeIndex
                if self.timeCompare(endTime, timeIndex):
                    break
                else:
                    continue

            '''found = re.search('PDLSI', line)
            if found:
                #key = line.split()[11]
                cpu = line.split()[8]
                mem = line.split()[9]
                dictVal = {'PDLSI': [cpu, mem]}
                dictCpu[dictKey] = dictVal
                print dictCpu
                #row = dictKey + ',' + cpu + ',' + mem'''
            
            dictVal = self.parseLine(dictKey, line)
            if dictVal:
                dictCpu[dictKey] = dictVal
                print dictCpu
        with open('test.csv', 'wb') as csvfile:
            csvfile.truncate()
            spam = csv.writer(csvfile, dialect='excel')
            spam.writerow(['Time','PDLSI cpu','PDLSI mem'])
            for key in dictCpu:
                sth = dictCpu[key][0:]
                sth.insert(0, key)
                spam.writerow(sth)
            csvfile.close()

        myFile.close()
        return dictCpu

    def parseLine(self, dictKey, line):
        found = re.search('PDLSI', line)
        if found:
            #key = line.split()[11]
            cpu = line.split()[8]
            mem = line.split()[9]
            dictVal = [cpu, mem]
            return dictVal
        else:
            pass

    def getFileList(self, lab, dir):
        '''
        get files from lab
        '''
        #cmd = "mdkir -f tmp4CPU"
        #os.popen(cmd)
        #cmd = "scp "+dir+"top* tmp4CPU"
        #os.popen(cmd)
        
        fileList = ""
        cmd = "ls "+dir+" | grep ^top | grep log$ | grep L | grep -v parsed"
        #cmd = "ls "+dir+" | grep ^top | grep log$"
        #cmd = "ls "+dir+" | grep test.txt"
        result = os.popen(cmd).read()
        output = result.strip().split(os.linesep)

        return output

    def cptAnaAll(self, startTime, endTime, lab, dir):
        '''
        '''
        dict={}
        for fileIndex in self.getFileList(lab, dir):
            print fileIndex
            fileIndex = dir+'/'+fileIndex
            result = self.cpuAna(startTime, endTime, fileIndex)
            bladeNumber = 1
            dict[bladeNumber] = result
        return dict
    
    def anaAll(self, dict):
        pass

cpuAnaAManager =  CPUAnaAManager()
dict1 = cpuAnaAManager.cptAnaAll('16:43:42', '16:43:48', 'atca47', './rawdata')
cpuAnaAManager.anaAll(dict1)




