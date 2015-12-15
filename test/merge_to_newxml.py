'''
Created on 2015.12.12

@author: dadl
'''
import os
import sys
import re
import commands
import lxml.etree

class MergeToNewxml(object):
    '''
    classdocs
    '''
    hardwaretype = ''
    msghnumbertemp, nrglisttemp, zonelisttemp, farmtcplisttemp, farmsctplisttemp = [],[],[],[],[] 

    def __init__(self):
        '''
        Constructor
        '''
    def mergeFile(self, oldxml, newxml):
        '''
        1. parse old SDM_General_Data.xml to dict:dictvalue
            # dictvalue example:
            # key: ('module', 'IP_conf', 'function', 'STATION_Setting', 'option', '0-0-11.MAC1')
            # value: '00:11:3f:ce:f3:4d'
        2. get hardware, nrglist, zone, nonpilot, msgh, Farm_TCP_list, Farm_SCTP_list.
            # Execute: cd <download_directory>/SDM_tools/ip_config 
            # Where <download_directory> is the location that the SDM_tools have been downloaded and installed.
            # Execute:    python ./gen_siteinfo.py -t <opt_string> ../cfg/SDM_General_Data_template.xml 
            # Note:  SDM_General_Data_template.xml was named SDM_General_Data.xml before.
            # <opt_string> format:
            # hardware=[hardware type]
            # Supported hardware type:ROUZIC, BONO24, BONO48, HPG6, or HPG8
            # nrglist=[nrglist]
            # nrglist for NRG network, valid format will be nrglist=1,2,3,4
            # zone=[zonelist]
            # zonelist for a NRG network, valid value will be 1,2,3
            # nonpilot=[num]
            # number of non-pilot station, valid value will be 2, 4, 6, 8, 10, 12, 14
            # msgh=[msghlist]
            # msghlist for FE  network, valid format will be msgh=1,2,3
            # Farm_TCP_list=[Farm_TCP_list]
            # valid format will be Farm_TCP_list=1,2,3,4
            # Farm_SCTP_list=[Farm_SCTP_list]
            # valid format will be Farm_SCTP_list=1,2 or Farm_SCTP_list=0 if there is no need for the SCTP configuration
            # For example, the following command:
            # python ./gen_siteinfo.py -t "hardware=ROUZIC nrglist=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22 zone=1,2 nonpilot=10 Farm_TCP_list=1,2" ../cfg/SDM_General_Data_template.xml
            # Generates .../cfg/SDM_General_Data.xml file, a template for a Rouzic system with 22 NRGs, 2 zones in each NRG, 10 non-pilot stations per NE,
            # 
            # python ./gen_siteinfo.py -t "hardware=BONO24 nrglist=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22 zone=1,2 nonpilot=10 msgh=1,2 Farm_TCP_list=1,2" ../cfg/SDM_General_Data_template.xml
            # generates .../cfg/SDM_General_Data.xml file, a template for a Bono system with 22 NRGs, 2 zones in each NRG, 10 non-pilot stations per NE, and 2 MSGH clusters. 
        3. generate new SDM_General_Data.xml based on result in step2 and new SDM_General_Data_template.xml
        4. parse new xml file into newdoc = lxml.etree.parse(newxml)
           get firstlevel.tag/name, secondlevel.tag/name, thirdlevel.tag/name
           xpath to find if the data exists in old xml
           if yes, set to newdoc thirdlevel.set('version', result)
            # datavalue = '//'+firstlevel.tag+'[@name="%s"]/'+secondlevel.tag+'[@name="%s"]/'+thirdlevel.tag+'[@name="%s"]'
            # result = olddoc.xpath(datavalue %(firstlevel.get('name'), secondlevel.get('name'), thirdlevel.get('name')))
            # if result yes
            # thirdlevel.set('version', result)
        5. write to new SDM_General_Data-[lab name].xml file newdoc.write('SDM_General_Data-[lab name].xml')
           Below method can add xml file first line <?xml version='1.0' encoding='UTF-8'?>
           newdoc.write('bono10.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
        '''      
        # 1. parse old SDM_General_Data.xml to dict:dictvalue
        dictvalue = {}
        doc = lxml.etree.parse(oldxml)

        for firstlevel in doc.getroot():
            #print (firstlevel.tag, firstlevel.attrib)
            for secondlevel in firstlevel:
                secondlevelname = secondlevel.get('name')
                msghfound = re.search(r'msgh(\d+)_Traffic_IPV4', secondlevelname)
                if msghfound:
                    self.msghnumbertemp.append(msghfound.group(1))
                nrg = re.search(r'BE.NETWORK.NRG.(\d+).*_IPV4', secondlevelname)
                if nrg:
                    self.nrglisttemp.append(nrg.group(1))
                zone = re.search(r'BE.NETWORK.NRG.1.ZONE.(\d+)_IPV4', secondlevelname)
                if zone:
                    self.zonelisttemp.append(zone.group(1))
                farmtcp = re.search(r'Farm_TCP(\d+)', secondlevelname)
                if farmtcp:
                    self.farmtcplisttemp.append(farmtcp.group(1))
                farmsctp = re.search(r'Farm_SCTP(\d+)', secondlevelname)
                if farmsctp:
                    self.farmsctplisttemp.append(farmsctp.group(1))
                for thirdlevel in secondlevel:
                    datavalue = '//'+firstlevel.tag+'[@name="%s"]/'+secondlevel.tag+'[@name="%s"]/'+thirdlevel.tag+'[@name="%s"]/@value'
                    test = doc.xpath(datavalue %(firstlevel.get('name'), secondlevel.get('name'), thirdlevel.get('name')))
                    dictvalue[(firstlevel.tag, firstlevel.get('name'), secondlevel.tag, secondlevel.get('name'), thirdlevel.tag, thirdlevel.get('name'))] = thirdlevel.get('value')
        # 2. get hardware type, zone id, msgh number, NRG number etc.          
        self.hardwaretype = doc.xpath(datavalue %('General', 'Common', 'HARDWARE'))[0]
        print 'Hardware type is: %s'%self.hardwaretype
        self.nrglisttemp = list(set(self.nrglisttemp))
        self.nrglisttemp.sort()
        nrglist = self.nrglisttemp[0]
        for i in self.nrglisttemp[1:]:
            nrglist += ','+i
        self.zonelisttemp = list(set(self.zonelisttemp))
        self.zonelisttemp.sort()
        zone = self.zonelisttemp[0]
        for i in self.zonelisttemp[1:]:
            zone += ','+i
        self.msghnumbertemp.sort()
        msgh = self.msghnumbertemp[0]        
        for i in self.msghnumbertemp[1:]:
            msgh += ','+i
        self.farmtcplisttemp = list(set(self.farmtcplisttemp))
        self.farmtcplisttemp.sort()
        farmtcplist = self.farmtcplisttemp[0]
        for i in self.farmtcplisttemp[1:]:
            farmtcplist += ','+i      
        self.farmsctplisttemp = list(set(self.farmsctplisttemp))
        self.farmsctplisttemp.sort()
        farmsctplist = self.farmsctplisttemp[0]
        for i in self.farmsctplisttemp[1:]:
            farmsctplist += ','+i
        #print 'farmsctp parameter is: %s'%farmsctplist
        nonpilotpar = ''

        # 3. generate new SDM_General_Data.xml based on result in step2 and new SDM_General_Data_template.xml
        #    dictpar example: hardware=BONO24 zone=1,2 Farm_SCTP_list=1 nonpilot=2 nrglist=1,2 Farm_TCP_list=1 msgh=1,2        
        hardware = self.hardwaretype
        dictpar = {}
        dictpar['nrglist'] = nrglist
        dictpar['zone'] = zone
        dictpar['msgh'] = msgh
        dictpar['Farm_TCP_list'] = farmtcplist
        dictpar['Farm_SCTP_list'] = farmsctplist
        dictpar['nonpilot'] = ''
        parstr = 'hardware=%s'%hardware
        for key in dictpar:
            if dictpar[key] != '':
                parstr += ' %s=%s'%(key, dictpar[key])
        cmd = 'python ./gen_siteinfo.py -t "%s" ../cfg/SDM_General_Data_template.xml'%parstr
        print cmd
        result = commands.getstatusoutput(cmd)[0]
        if result != 0:
            print 'Command:"%s" execute failed!'%cmd
            sys.exit(2)
        # 4. parse new xml file into newdoc = lxml.etree.parse(newtemplate)
        newxmltemp = '../cfg/SDM_General_Data.xml'
        newdoc = lxml.etree.parse(newxmltemp)
        for firstlevel in newdoc.getroot():
            for secondlevel in firstlevel:
                for thirdlevel in secondlevel:
                    #datapath = '//'+firstlevel.tag+'[@name="%s"]/'+secondlevel.tag+'[@name="%s"]/'+thirdlevel.tag+'[@name="%s"]/@value'
                    datapath = '//'+firstlevel.tag+'[@name="%s"]/'+secondlevel.tag+'[@name="%s"]/'+thirdlevel.tag+'[@name="%s"]'
                    datavalue = datapath+'/@value'
                    test = doc.xpath(datavalue %(firstlevel.get('name'), secondlevel.get('name'), thirdlevel.get('name')))
                    if test:
                        if test[0] != '':
                            thirdlevel.set('value', test[0])
        # 5. write to new SDM_General_Data-[lab name].xml file newdoc.write('SDM_General_Data-[lab name].xml')
        newdoc.write('../cfg/%s'%newxml, pretty_print=True, xml_declaration=True, encoding='utf-8')
        print 'New xml file "%s" generated under ../cfg!'%newxml
        '''# write to new xmltree.xml file after update(set) value
        test = 'atca23'
        doc.write(newxml)
        '''
        
    def parseArg(self):
        if len(sys.argv) != 3:
            print 'Agument number wrong! You need to input 2 parameters!\n'\
                  'E.g. SDM_General_Data_bono10.xml SDM_General_Data_atca23.xml\n'\
                  '     First parameter is old xml file, second one is new generated xml file name.'
            sys.exit(0)
        else:
            oldxml = sys.argv[1]
            newxml = sys.argv[2]
            return oldxml, newxml

if __name__=='__main__':
    mergeToNewxml = MergeToNewxml()
    result = os.path.exists('./gen_siteinfo.py')
    if not result:
        print 'You need to run this script under same folder with "gen_siteinfo.py"!'
        sys.exit(1)
    oldxml, newxml = mergeToNewxml.parseArg()
    oldxmlexist = os.path.exists(oldxml)
    if not oldxmlexist:
        print 'Old xml "%s" does not exist!'%oldxml
        sys.exit(1)
    mergeToNewxml.mergeFile(oldxml, newxml)