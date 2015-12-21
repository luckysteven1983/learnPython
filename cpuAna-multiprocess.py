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
import threading
import datetime
from time import sleep
import xlsxwriter
from lib.ssh import ssh_manager

class CPUAnaAManager(object):
    '''
    classdocs 
    '''
    dictCpu = {}
    dictName = {}
    dictTime = {}
    dictRow = {}
    dictSheet = {}
    dictSecond = {}
    dictSta = {}
    for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
        dictName[i] = dictCpu
        dictTime[i] = []
        dictRow[i] = 0
        dictSecond[i] = []
        dictSta[i] = ''
    dictKey = ''
    dictChart = {}
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
    def cpuAna(self, startTime, endTime, fileInput, fileName):
        '''
        '''
        #print 'Start processing station: %s'%fileName
        dictCpu = {}
        self.dictTime[fileName] = []
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
                self.dictTime[fileName].append(timeIndex)
                if not self.timeCompare(timeIndex, endTime):
                    break
                else:
                    dictCpu[dictKey] = {}
                    continue

            for keyVal in ['Cpu0', 'Cpu1', 'Mem', 'Swap', 'OamCOMM',
                 'PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']:
                check = re.search(keyVal, line)
                if check:
                    if keyVal in ['OamCOMM', 'PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']:
                    #print "PDLSI1 line: %s"%line
                        cpuMem = self.parseProcess(keyVal, line)
                        dictCpu[dictKey][keyVal] = cpuMem
                    elif keyVal in ['Cpu0', 'Cpu1']:
                        cpu = self.parseCpu(keyVal, line)
                        if keyVal in ['Cpu0']:
                            cpu0 = cpu
                            dictCpu[dictKey][keyVal] = [cpu0]
                        if keyVal in ['Cpu1']:
                            cpu1 = cpu
                            dictCpu[dictKey][keyVal] = [cpu1]
                            cpuAve = round((cpu0+cpu1)/2, 1)
                            dictCpu[dictKey]['Cpu_Ave'] = [cpuAve]
                    elif keyVal in ['Mem']:
                        mem = round(self.parseMem(keyVal, line)/1024, 1)
                    elif keyVal in ['Swap']:
                        swap = round(self.parseSwap(keyVal, line)/1024, 1)
                        realmem = round(swap+mem, 1)
                        dictCpu[dictKey]['Mem'] = [round(swap+mem, 1)]
                else:
                    if keyVal in ['OamCOMM', 'PDLSI1', 'PDLSL1', 'PDLSU1', 'PDLSM1']:
                        if not dictCpu[dictKey].has_key(keyVal):
                            dictCpu[dictKey][keyVal] = [0,0]
                    if keyVal in ['Cpu0', 'Cpu1', 'Mem', 'Swap',]:
                        if not dictCpu[dictKey].has_key(keyVal):
                            dictCpu[dictKey][keyVal] = [0]
        myFile.close()
        self.dictName[fileName] = dictCpu
        #print 'End processing station: %s'%fileName
        #self.dictTime[fileName] = self.allTime[fileName]
        return self.dictName[fileName]

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
        
    def writeToSheet(self, workbook, sheetName, name):
        ### Use xlsxwriter to create worksheet ###
        #print 'Start processing sheet: %s'%sheetName

            #chart = workbook.add_chart({'type': 'line', 'name': sheetName+'_cpu'})
            #self.dictChart[fileName] = workbook.add_chart({'type': 'line', 'name': fileName})
                
        second = []
        for keykey in self.dictTime[name][0:-1]:
            sth = []
            keyCpu = self.dictName[name][keykey]
            for parseItem in self.parseList:
                sth += keyCpu[parseItem]
            sth.insert(0, keykey)
            second.append(tuple(sth))
        second.insert(0, tuple(self.firstRow))
        self.dictSecond[name] = second
                
#         booksheet1 = workbook.add_worksheet('Sta_'+name)
#         #chart = workbook.add_chart({'type': 'line', 'name': sheetName+'_cpu'})
#         #self.dictChart[fileName] = workbook.add_chart({'type': 'line', 'name': fileName})        
#         second = []
#         for keykey in self.dictTime[name][0:-1]:
#             sth = []
#             keyCpu = self.dictName[name][keykey]
#             for parseItem in self.parseList:
#                 sth += keyCpu[parseItem]
#             sth.insert(0, keykey)
#             second.append(tuple(sth))
#         print name, second[-10:]
#         second.insert(0, tuple(self.firstRow))
#         for i, row in enumerate(second):
#             for j, col in enumerate(row):
#                 booksheet1.write(i, j, col)
#         self.dictRow[name] = len(self.dictName[name].keys()) + 1
#         #rowNum = 4000
#         chart.add_series({'name': '='+sheetName+'!$B$1',
#                           'categories': '='+sheetName+'!$A$2:$A$'+str(self.dictRow[name]),
#                           'values': '='+sheetName+'!$B$2:$B$'+str(self.dictRow[name])})
#         chart.add_series({'name': '='+sheetName+'!$C$1',
#                           'categories': '='+sheetName+'!$A$2:$A$'+str(self.dictRow[name]),
#                           'values': '='+sheetName+'!$C$2:$C$'+str(self.dictRow[name])})
#         self.dictSheet[name].insert_chart('B10', chart)
        #print 'End processing sheet: %s'%sheetName
#         self.dictSheet[name] = booksheet1
#         return self.dictSheet[name]
        #booksheet1.col(0).width=10

    def getFileList(self, lab, dir):
        '''
        get files from local directory       
        '''      
        fileList = ""
        #cmd = "ls "+dir+" | grep ^top | grep log$ | grep D | grep -v parsed"
        cmd = "ls "+dir+" | grep ^top | grep log$ | grep -v parsed"
        #cmd = "dir /B .\cache\%s"%lab
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
#         for self.fileName in self.getFileList(lab, dir):
#             fileIndex = dir+'/'+self.fileName
#             self.fileName = re.search(r'top_(\w).', self.fileName).group(1)
#             self.dictCpu = {}
#             result = self.cpuAna(startTime, endTime, fileIndex)
#             self.writeToSheet(workbook, 'Sta_'+self.fileName, result)
        loops = self.getFileList(lab, dir)
        threads2 = []
        loop = range(len(loops))
        for i in loop:
            fileIndex = dir+'/'+loops[i]
            name = re.search(r'top_(\w).', loops[i]).group(1)
            #result = self.cpuAna(startTime, endTime, fileIndex, name)
            t2 = threading.Thread(target=self.cpuAna, args=(startTime, endTime, fileIndex, name))
            #self.writeToSheet(workbook, 'Sta_'+name, self.dictName[name])
            #t2 = threading.Thread(target=self.writeToSheet, args=(workbook, 'Sta_'+name, self.dictName[name], name))
            threads2.append(t2)
        print threads2
        for i in loop:
            threads2[i].start()
        for i in loop:
            threads2[i].join()
        
        threads1 = []
        for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
            self.dictSheet[i] = workbook.add_worksheet('Sta_'+i)
        #chart = workbook.add_chart({'type': 'line'})
        for j in loop:
            fileIndex = dir+'/'+loops[j]
            name = re.search(r'top_(\w).', loops[j]).group(1)
            t1 = threading.Thread(target=self.writeToSheet, args=(workbook, 'Sta_'+name, name))
            threads1.append(t1)
        print threads1
        for j in loop:
            threads1[j].start()
        for j in loop:
            threads1[j].join()
        
        for i in loop:
            fileIndex = dir+'/'+loops[i]
            name = re.search(r'top_(\w).', loops[i]).group(1)    
            for i, row in enumerate(self.dictSecond[name]):
                for j, col in enumerate(row):
                    self.dictSheet[name].write(i, j, col)        
            rowNum= len(self.dictName[name].keys()) + 1
            sheetName = 'Sta_'+name
            chart = workbook.add_chart({'type': 'line'})
            chart.add_series({'name': '='+sheetName+'!$B$1',
                              'categories': '='+sheetName+'!$A$2:$A$'+str(rowNum),
                              'values': '='+sheetName+'!$B$2:$B$'+str(rowNum)})
            chart.add_series({'name': '='+sheetName+'!$C$1',
                              'categories': '='+sheetName+'!$A$2:$A$'+str(rowNum),
                              'values': '='+sheetName+'!$C$2:$C$'+str(rowNum)})
            self.dictSheet[name].insert_chart('B10', chart)

        #print '%s: Write data into excel START!'%datetime.datetime.now()
        workbook.close()
        #print '%s: Write data into excel DONE!'%datetime.datetime.now()
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
    print '---test cpuAna-multiprocess.py starts!---\n'\
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
        print datetime.datetime.now()
        dict1 = cpuAnaAManager.cptAnaAll(arg[0], arg[1], lab, './cache/'+lab)
        #dict1 = cpuAnaAManager.cptAnaAll('14:51:00', '14:53:00', lab, './cache/'+lab)
        print '---parse '+lab+' data done!---'
    print datetime.datetime.now()
    print '---test is done!---'
    #cpuAnaAManager.anaAll(dict1)
    #python cpuAna.py '17:25:00' '20:30:00' 'atca23, atca43, atca55, atca45, atca47, atca57, atca58, atca56, atca59, atca19' '/PLATsoftware/pt_result/2015-12-16/fm1951'