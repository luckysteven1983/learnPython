# -*- coding: cp936 -*-
'''
Created on Dec 5, 2015

@author: Da
'''
import re
import os
import csv
#import xlwt
import xlsxwriter

class CPUAnaAManager(object):
    '''
    classdocs 
    '''
    dictCpu = {}
    output = {}
    dictKey = ''
    allTime = []
    #parseList = ['PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']
    
    parseList = ['Cpu0', 'Cpu1', 'Cpu_Ave', 'Mem', 'PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']
    firstRow = ['Time', 'SysCPU_0', 'SysCPU_1', 'SysCPU_AVE', 'Mem', 'PDLSI1_cpu','PDLSI1_mem','PDLSL1_cpu','PDLSL1_mem','PDLSU1_cpu','PDLSU1_mem','PDLSM1_cpu','PDLSM1_mem',]

    def __init__(self):
        '''
        Constructor
        '''
    def timeCompare(self, time1, time2):
        '''
        True is <=
        '''
        if cmp(time1, time2) <= 0:
            return True
        else:
            return False
    def cpuAna(self, startTime, endTime, fileInput):
        '''
        '''
        self.allTime = []
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
                self.dictKey = timeIndex
                self.allTime.append(timeIndex)
                if not self.timeCompare(timeIndex, endTime):
                    break
                else:
                    self.dictCpu[self.dictKey] = {}
                    continue
                
            for keyVal in ['Cpu0', 'Cpu1', 'Cpu_Ave', 'Mem', 'Swap', 'PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']:
                check = re.search(keyVal, line)
                if check:
                    if keyVal in ['PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']:
                    #print "PDLSI1 line: %s"%line
                        cpuMem = self.parseProcess(keyVal, line)
                        self.dictCpu[self.dictKey][keyVal] = cpuMem
                    if keyVal in ['Cpu0', 'Cpu1']:
                        cpu = self.parseCpu(keyVal, line)
                        if keyVal in ['Cpu0']:
                            cpu0 = cpu
                            self.dictCpu[self.dictKey][keyVal] = [cpu0]
                        if keyVal in ['Cpu1']:
                            cpu1 = cpu
                            self.dictCpu[self.dictKey][keyVal] = [cpu1]
                            cpuAve = (cpu0+cpu1)/2
                            self.dictCpu[self.dictKey]['Cpu_Ave'] = [cpuAve]
                    if keyVal in ['Mem']:
                        mem = round(self.parseMem(keyVal, line)/1024, 1)
                        #self.dictCpu[self.dictKey][keyVal] = mem
                    if keyVal in ['Swap']:
                        swap = round(self.parseSwap(keyVal, line)/1024, 1)
                        self.dictCpu[self.dictKey]['Mem'] = [swap+mem]

        '''with open('test.csv', 'wb') as csvfile:
            csvfile.truncate()
            spam = csv.writer(csvfile, dialect='excel')
            spam.writerow(self.firstRow)
            for key in self.dictCpu:
                if self.timeCompare(endTime, key):
                    continue
                else:
                    sth = []
                    keyCpu = self.dictCpu[key]
                    for parseItem in self.parseList:
                        sth += keyCpu[parseItem]
                    sth.insert(0, key)
                    spam.writerow(sth)
            csvfile.close()'''

        myFile.close()
        return self.dictCpu

    def parseCpu(self, keyValue, line):
        cpu = re.search(r'.: (\d+\.\d)%us.', line).group(1)
        dictVal = float(cpu)
        return dictVal

    def parseMem(self, keyValue, line):
        mem = re.search(r'.(\d+)k buffers', line).group(1)
        dictVal = float(mem)
        return dictVal
    
    def parseSwap(self, keyValue, line):
        swap = re.search(r'.(\d+)k cached', line).group(1)
        dictVal = float(swap)
        return dictVal

    def parseProcess(self, keyValue, line):
        cpu = line.split()[8]
        mem = line.split()[9]
        dictVal = [float(cpu), float(mem)]
        return dictVal
        
    def writeToSheet(self, workbook, sheetName, dictCpu):
        booksheet1 = workbook.add_worksheet(sheetName)
        chart = workbook.add_chart({'type': 'column'})
        second = []
        third = []
        for key in self.allTime[0:-1]:
            sth = []
            keyCpu = dictCpu[key]
            for parseItem in self.parseList:
                sth += keyCpu[parseItem]
            sth.insert(0, key)
            second.append(tuple(sth))
        second.insert(0, tuple(self.firstRow))
        for i, row in enumerate(second):
            for j, col in enumerate(row):
                booksheet1.write(i, j, col)

        chart.add_series({'values': '='+sheetName+'!$A$2:$A$3'})
        chart.add_series({'values': '='+sheetName+'!$B$2:$B$3'})
        booksheet1.insert_chart('E2', chart)
        return booksheet1
        #booksheet1.col(0).width=10

    def getFileList(self, lab, dir):
        '''
        get files from lab
        '''
        #cmd = "mdkir -f tmp4CPU"
        #os.popen(cmd)
        #cmd = "scp "+dir+"top* tmp4CPU"
        #os.popen(cmd)
        
        fileList = ""
        cmd = "ls "+dir+" | grep ^top | grep log$ | grep 16_43 | grep -v parsed"
        #result = os.popen(cmd).read()
        k = []
        for i in os.popen(cmd).readlines():
            j = i.strip()
            k.append(j)
        #output = result.strip().split(os.linesep)
        print k
        return k

    def cptAnaAll(self, startTime, endTime, lab, dir):
        '''
        '''
        print '---test---'
        #workbook = xlwt.Workbook(encoding='utf-8')
        workbook = xlsxwriter.Workbook('result.xlsx')
        for fileName in self.getFileList(lab, dir):
            fileIndex = dir+'/'+fileName
            fileName = re.search(r'top_(\w).', fileName).group(1)
            self.dictCpu = {}
            result = self.cpuAna(startTime, endTime, fileIndex)
            self.writeToSheet(workbook, 'Sta_'+fileName, self.dictCpu)

            ### Use csv to create .csv text file method ###
            '''with open('test.csv', 'wb') as csvfile:
                csvfile.truncate()
                spam = csv.writer(csvfile, dialect='excel')
                spam.writerow(self.firstRow)
                for key in self.dictCpu:
                    sth = []
                    keyCpu = self.dictCpu[key]
                    for parseItem in self.parseList:
                        sth += keyCpu[parseItem]
                    sth.insert(0, key)
                    print 'sth: ',sth
                    spam.writerow(sth)
            csvfile.close()'''
            ### Use worksheet to create .xls excel file method ###
            '''workbook = xlwt.Workbook(encoding='utf-8')
            booksheet1 = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
            booksheet2 = workbook.add_sheet('Sheet 2')
            second = []
            third = []
            for key in self.dictCpu:
                sth = []
                keyCpu = self.dictCpu[key]
                for parseItem in self.parseList:
                    sth += keyCpu[parseItem]
                sth.insert(0, key)
                second.append(tuple(sth))
            second.insert(0, tuple(self.firstRow))
            print second
            for i, row in enumerate(second):
                for j, col in enumerate(row):
                    booksheet1.write(i, j, col)
            booksheet1.col(0).width=10
            
            self.writeToSheet(workbook, fileName, self.dictCpu)
            workbook.save('result.xls')'''
        workbook.close()
            
            #bladeNumber = 1
            #self.output[bladeNumber] = result
        return dict
    
    def anaAll(self, dict):
        pass

cpuAnaAManager =  CPUAnaAManager()
dict1 = cpuAnaAManager.cptAnaAll('16:43:42', '16:43:44', 'atca47', './rawdata')
cpuAnaAManager.anaAll(dict1)




