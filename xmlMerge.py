import xml.dom.minidom
import os
import sys
import re
import fileinput
import argparse

try:
    import xml.etree.cElementTree as ET
except ImportError:
    print ("ImportError")
    import xml.etree.ElementTree as ET

class XMLMerge():
    
    '''
    '''

    
    def __init__(self,fileName):
        Doctree=ET.parse(fileName)
        root=Doctree.getroot()
        self.root=root
        self.xmlDict=self.xmlToDict(fileName)
        '''
        
        '''

    def xmlToDict(self,fileName):
        dictRoot={}
        dictL1={}
        dictL2={}

        
        for childL1 in self.root:
            keyL1=childL1.attrib.get('name')
            #print ('=========keyL1 is  ',childL1.attrib)
            dictL1={}
            for childL2 in childL1:
                
                keyL2=childL2.attrib.get('name')
                #print ('=========keyL2 is  ',childL2.attrib)
                dictL2={}
                for childL3 in childL2:
                    keyL3=childL3.attrib.get('name')
                    valueL3=childL3.attrib.get('value')
                    dictL2[keyL3]=valueL3
                #print dictL2
                dictL1[keyL2]=dictL2
            dictRoot[keyL1]=dictL1
            #xmlDict=dictRoot

        return dictRoot
        #verify the dict is correct
        '''
        for key in dictRoot:
            print("==============level1 key is",key)
            for key2 in dictRoot.get(key):
                print("===================level2 key is",key2)    
         '''
    def getValueFromDict(self,module,function,option):
        
        if self.xmlDict.has_key(module):
            if self.xmlDict.get(module).has_key(function):
                if self.xmlDict.get(module).get(function).has_key(option):
                    #print("===========",module,function,option)
                    returnValue=self.xmlDict.get(module).get(function).get(option)
                    #print (returnValue)
                    return returnValue
        return "Invalid"
        '''
        return self.xmlDict.get(module).get(function).get(option)
        '''
        
    def generateNewXml(self,fileName,targetFileName):
        print('+'*80)
        print("Generate new configuration file for this release, the file name is: ")
        print(targetFileName)
        fp=open(fileName,'r+')
        tFp=open(targetFileName,'w')
        done=0
        lineNum=0
        #flag=0
        while not done:
            line=fp.readline()
            tFp.write(line)
            lineNum=lineNum+1
            #print(lineNum)
            if(line==''):
                done=1
            else:
                if re.search('<module',line):
                    module=self.getAttribFromTag(line)
                    continue
                if re.search('<function',line):
                    function=self.getAttribFromTag(line)
                    continue
                if re.search('<option name=\"',line):
                    option=self.getAttribFromTag(line)
                #print("module=%s,function=%s,option=%s"%(module,function,option))
                    value=self.getValueFromDict(module, function, option)
                #print (option," == ",value)
                #print ("============value is=========",value)
                    if value=="Invalid":
                        continue
                    else:
                        strTo=re.sub('\"\"','\"'+str(value)+'\"',line)
                    #line=line.replace(line,strTo)
                #print("==============",strTo)
                    #print("lineNum is %d",lineNum)
                    #print("strTo is %s"%strTo)
                        tFp.seek(-len(line),1)
                        ss=line.replace(line,strTo)
                        tFp.writelines(ss)
                    #fp.readline()
                    continue
        fp.close()
        tFp.close()
                
    
    def getAttribFromTag(self,line):
        aa=line.split('name=\"')[1].split('\"')[0]
        return aa
    
    def getHardwareTypeFromXmlDict(self):
        return self.xmlDict.get("General").get("Common").get("HARDWARE")
        '''
        '''
    def getSystemPrefixFromXmlDict(self):
        return self.xmlDict.get("IP_conf").get("Common").get("SYSTEM_PREFIX")
    
    def getZoneListFromXmlDict(self):
        zoneList=[]
        for zoneid in [3,2,1]:
            myStr="BE.NETWORK.NRG.1.ZONE."+str(zoneid)+"_IPV4"
            if self.xmlDict.get("IP_conf").has_key(myStr):
                zoneList.append(str(zoneid))
        zoneList.sort()
        return zoneList

    def getNRGListFromXmlDict(self):
        nrgList=[]            
        for nrgid in [10,9,8,7,6,5,4,3,2,1]:
            myStr="BE.NETWORK.NRG."+str(nrgid)+".ZONE.2_IPV4"
            if self.xmlDict.get("IP_conf").has_key(myStr):
                nrgList.append(str(nrgid))
        nrgList.sort()
        return nrgList
        
            
    def getMsghListFromXmlDict(self):
        msghList=[]
        for msghid in [10,9,8,7,6,5,4,3,2,1]:
            myStr="MSGH_Cluster.FE."+str(msghid)+"_IPV4"
            if self.xmlDict.get("IP_conf").has_key(myStr):
                msghList.append(str(msghid))
        if len(msghList)==0:
            msghList=['0']
        else:
            msghList.sort()
        return msghList       
    
    def getFarmTCPListFromXmlDict(self):
        farmTcpList=[]
        for farmTcpId in [10,9,8,7,6,5,4,3,2,1]:
            myStr="Farm_TCP"+str(farmTcpId)
            if self.xmlDict.get("LB").has_key(myStr):
                farmTcpList.append(str(farmTcpId))
                #print farmTcpList
        if len(farmTcpList)==0:
            farmTcpList=['0']
        else:
            farmTcpList.sort()
        #print ("farm is ",farmTcpList)
        return farmTcpList
         
    
    def getFarmSCTPListFromXmlDict(self):
        farmSCTPList=[]
        for farmSctpId in [10,9,8,7,6,5,4,3,2,1]:
            myStr="Farm_SCTP"+str(farmSctpId)
            if self.xmlDict.get("LB").has_key(myStr):
                farmSCTPList.append(str(farmSctpId))
        if len(farmSCTPList)==0:
            farmSCTPList=['0']
        else:
            farmSCTPList.sort()
        return farmSCTPList
    
    
    def generateNewTemplate(self):
        '''
        '''
        cmd=self.generateTemplateCmd()
        r=os.popen(cmd)
        text=r.read()
        print(text)
        r.close()
        
    def generateTemplateCmd(self):
        
        hardware=self.getHardwareTypeFromXmlDict()
        lab=self.getSystemPrefixFromXmlDict()
        nrgList=self.getNRGListFromXmlDict()
        nrgListStr=' nrglist='+','.join(nrgList)
        msghList=self.getMsghListFromXmlDict()
        msghListStr=' msgh='+','.join(msghList)
        zoneList=self.getZoneListFromXmlDict()
        zoneListStr=' zone='+','.join(zoneList)
        farmTcpList=self.getFarmTCPListFromXmlDict()
        farmTcpListStr=' Farm_TCP_list='+','.join(farmTcpList)
        farmSctpList=self.getFarmSCTPListFromXmlDict()
        farmSctpListStr=' Farm_SCTP_list='+','.join(farmSctpList)
        print('*'*80)
        print("Generate template for this lab according to the old configuration File:")
        '''
        python ./gen_siteinfo.py -t "hardware=BONO24
        nrglist=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,
        22 zone=1,2 nonpilot=10 msgh=1,2
        Farm_TCP_list=1,2" ../cfg/SDM_General_Data_template.xml
        '''
        myStr='python ../ip_config/gen_siteinfo.py -t '
        option='\"hardware='+hardware+nrgListStr+msghListStr+zoneListStr+farmTcpListStr+farmSctpListStr+'\"'
        cmd=myStr+option+' ./SDM_General_Data_template.xml'
        
        print(cmd)
        print "\nTemplate is generated at: "
        return cmd
    
    def generateInstallationFiles(self,fileName):
        lab=self.getSystemPrefixFromXmlDict()
        os.popen("mkdir -p "+lab)
        
        '''
        ../ip_config/gen_siteinfo.py -s ../ip_config/siteinfo.template -o . SDM_General_Data.xml

        '''
        cmd='../ip_config/gen_siteinfo.py -s ../ip_config/siteinfo.template -o '+lab+' ./'+fileName
        
        print('\n\nSTEP.3')
        print('*'*80)
        print cmd
        r=os.popen(cmd)
        text=r.read()
        print(text)
        cpCmd='cp -rf '+fileName+' '+lab
        os.popen(cpCmd)
        r.close()
        
           
    @staticmethod
    def _argvParse():
        parser = argparse.ArgumentParser('''
        Examples: 
        =======================================================================
        python ./xmlMerge.py -oldXml SDM_General_Data.xml 
         =======================================================================
         ''')
        
        parser.add_argument('-oldXml', action='store', dest='oldFile', help='SDM_General_Data_BONO12.xml in old release',required=True)
        #parser.add_argument('-newTemplate', action='store', dest='template', help='New template xml file',required=True)
        #parser.add_argument('-o', action='store', dest='newFile', help='New output xml file(generated by this programme',required=True)
        result=parser.parse_args()
        return result                      
           
if __name__=='__main__':
    
    
    myArgu=XMLMerge._argvParse()
    oldFile=myArgu.oldFile
    #newTemplate=myArgu.template
    #newFile=myArgu.newFile
    if oldFile=='SDM_General_Data.xml':
        print('Error:\nOldFile name cannot be SDM_General_Data.xml, it is conflict with template generation file, please rename it')
        sys.exit()
    sdmXml=XMLMerge(oldFile)
    print('\nSTEP.1')
    sdmXml.generateNewTemplate()
    templateFileName='SDM_General_Data.xml'
    targetFileName=templateFileName.split('.')[0]+'_'+sdmXml.getSystemPrefixFromXmlDict()+'_NEW.'+templateFileName.split('.')[1]
    
    print('\nSTEP.2')
    sdmXml.generateNewXml(templateFileName, targetFileName)
    sdmXml.generateInstallationFiles(targetFileName)
 