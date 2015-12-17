#!/usr/bin/env python
# -*- coding: cp936 -*-
'''
Created on Dec 5, 2015

@author: Da
1. scpGetAll to get file from lab,dir
2. parse data
3. write data to excel(generate chart)/csv files

@version: 0.2
Modified at Dec 7th, 2015
Add sshManager(This function is from automation team code), get files from each lab, and parse to separate xlsx file.
'''
import re
import os
import sys
import csv
import datetime
import xlsxwriter
from lib.ssh import ssh_manager

class CPUAnaAManager(object):
    '''
    classdocs 
    '''
    dictCpu = {}
    dictKey = ''
    allTime = []
    fileName = ''
    parseList = ['Cpu0', 'Cpu1', 'Cpu_Ave', 'Mem', 'OamCOMM',
                 'PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']
    firstRow = ['Time', 'SysCPU_0', 'SysCPU_1', 'SysCPU_AVE', 'Mem', 'OamCOMM_cpu',
                'OamCOMM_mem', 'PDLSI1_cpu','PDLSI1_mem','PDLSL1_cpu','PDLSL1_mem',
                'PDLSU1_cpu','PDLSU1_mem','PDLSM1_cpu','PDLSM1_mem',]
    ssh = ssh_manager.SshManager()
    
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

            for keyVal in ['Cpu0', 'Cpu1', 'Mem', 'Swap', 'OamCOMM',
                 'PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']:
                check = re.search(keyVal, line)
                if check:
                    if keyVal in ['OamCOMM', 'PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']:
                    #print "PDLSI1 line: %s"%line
                        cpuMem = self.parseProcess(keyVal, line)
                        self.dictCpu[self.dictKey][keyVal] = cpuMem
                    elif keyVal in ['Cpu0', 'Cpu1']:
                        cpu = self.parseCpu(keyVal, line)
                        if keyVal in ['Cpu0']:
                            cpu0 = cpu
                            self.dictCpu[self.dictKey][keyVal] = [cpu0]
                        if keyVal in ['Cpu1']:
                            cpu1 = cpu
                            self.dictCpu[self.dictKey][keyVal] = [cpu1]
                            cpuAve = round((cpu0+cpu1)/2, 1)
                            self.dictCpu[self.dictKey]['Cpu_Ave'] = [cpuAve]
                    elif keyVal in ['Mem']:
                        mem = round(self.parseMem(keyVal, line)/1024, 1)
                    elif keyVal in ['Swap']:
                        swap = round(self.parseSwap(keyVal, line)/1024, 1)
                        realmem = round(swap+mem, 1)
                        self.dictCpu[self.dictKey]['Mem'] = [round(swap+mem, 1)]
                else:
                    if keyVal in ['OamCOMM', 'PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']:
                        if not self.dictCpu[self.dictKey].has_key(keyVal):
                            self.dictCpu[self.dictKey][keyVal] = [0,0]
                    if keyVal in ['Cpu0', 'Cpu1', 'Mem', 'Swap',]:
                        if not self.dictCpu[self.dictKey].has_key(keyVal):
                            self.dictCpu[self.dictKey][keyVal] = [0]

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
        cpu = re.search(r'.: +(\d+\.\d)%us.', line).group(1)
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
        found = re.search(keyValue, line)
        if found:
            cpu = line.split()[8]
            mem = line.split()[9]
            dictVal = [float(cpu), float(mem)]
            return dictVal
        
    def writeToSheet(self, workbook, sheetName, dictCpu):
        ### Use xlsxwriter to create worksheet ###
        booksheet1 = workbook.add_worksheet(sheetName)
        chart = workbook.add_chart({'type': 'line', 'subtype': 'percent_stacked'})
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
        rowNum = len(dictCpu.keys()) + 1
        chart.add_series({'name': '='+sheetName+'!$B$1',
                          'categories': '='+sheetName+'!$A$2:$A$'+str(rowNum),
                          'values': '='+sheetName+'!$B$2:$B$'+str(rowNum)})
        chart.add_series({'name': '='+sheetName+'!$C$1',
                          'categories': '='+sheetName+'!$A$2:$A$'+str(rowNum),
                          'values': '='+sheetName+'!$C$2:$C$'+str(rowNum)})
        booksheet1.insert_chart('B10', chart)
        return booksheet1
        #booksheet1.col(0).width=10

    def getFileList(self, lab, dir):
        '''
        get files from local directory       
        '''      
        fileList = ""
        #cmd = "ls "+dir+" | grep ^top | grep log$ | grep D | grep -v parsed"
        cmd = "ls "+dir+" | grep ^top | grep log$ | grep -v parsed"
        #result = os.popen(cmd).read()
        k = []
        for i in os.popen(cmd).readlines():
            j = i.strip()
            k.append(j)
        return k

    def getFilesFromLab(self, lab, dir):
        '''
        get files from lab       
        '''
        fileList = []
        fileList = self.ssh.scpGetAll(lab, dir+'/top_*.log')
        return fileList

    def cptAnaAll(self, startTime, endTime, lab, dir):
        '''
        1. create xlsx file
        2. getFileList
        3. parse one station data to dict dictCpu
        4. add data to worksheet by function writeToSheet
        5. close file to save it
        '''
        workbook = xlsxwriter.Workbook('result_'+lab+'.xlsx')
        for self.fileName in self.getFileList(lab, dir):
            fileIndex = dir+'/'+self.fileName
            self.fileName = re.search(r'top_(\w).', self.fileName).group(1)
            self.dictCpu = {}
            result = self.cpuAna(startTime, endTime, fileIndex)
            self.writeToSheet(workbook, 'Sta_'+self.fileName, result)

            ### Use csv to create .csv text file method ###
            '''with open('./cache/'+lab+'/result_'+lab+'_Sta_'+self.fileName+'.csv', 'wb') as csvfile:
                csvfile.truncate()
                spam = csv.writer(csvfile, dialect='excel')
                spam.writerow(self.firstRow)
                for key in self.dictCpu:
                    sth = []
                    keyCpu = self.dictCpu[key]
                    for parseItem in self.parseList:
                        sth += keyCpu[parseItem]
                    sth.insert(0, key)
                    #print 'sth: ',sth
                    spam.writerow(sth)
            csvfile.close()'''
            ### Use 'xlwt' worksheet to create .xls excel file method ###
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

    def parseArg(self):
        if len(sys.argv) != 5:
            print 'Agument number wrong! You need to input 4 parameters!\n'\
                  "'E.g. 16:43:42', '16:43:48', 'atca55, atca47', '/PLATsoftware/pt_result/2015-12-03/fm1945'"
            sys.exit(0)
        else:
            startTime = sys.argv[1]
            endTime = sys.argv[2]
            labList = sys.argv[3]
            directory = sys.argv[4]
            print startTime, endTime, labList, directory
            return startTime, endTime, labList, directory

if __name__=='__main__':
    cpuAnaAManager = CPUAnaAManager()
    arg = cpuAnaAManager.parseArg()
    print '---test starts!---\n'\
          '---parsing data from startTime: '+arg[0]+' to endTime: '+arg[1]+'---'           
    print datetime.datetime.now()
    labList = arg[2].split(',')
    for lab in list(labList):
        #fileFolder = '/PLATsoftware/pt_result/2015-12-03/fm1945_'+lab+'/Done/top_*.log'
        lab = lab.strip()
        cpuAnaAManager.ssh.getClient(lab)
        ifDir = cpuAnaAManager.ssh.run(lab, 'ls '+arg[3])
        if ifDir[0] == 0:
            fileFolder = arg[3]+'/Done'
        else:
            fileFolder = arg[3]+'_'+lab+'/Done'
        cpuAnaAManager.getFilesFromLab(lab, fileFolder)
        dict1 = cpuAnaAManager.cptAnaAll(arg[0], arg[1], lab, './cache/'+lab)
        #dict1 = cpuAnaAManager.cptAnaAll('14:51:00', '14:53:00', lab, './cache/'+lab)
        print '---parse '+lab+' data done!---'
    print datetime.datetime.now()
    print '---test is done!---'
    #cpuAnaAManager.anaAll(dict1)
    #python cpuAna.py '14:51:00', '14:53:00', 'atca55, atca47', '/PLATsoftware/pt_result/2015-12-03/fm1945_'



