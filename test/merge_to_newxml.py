'''
Created on 2015.12.12

@author: dadl
'''
import re
import lxml.etree

class MergeToNewxml(object):
    '''
    classdocs
    '''
    msghnumber = []
    hardwaretype = ''


    def __init__(self):
        '''
        Constructor
        '''
    def mergeFile(self):
        '''
        1. parse old SDM_General_Data.xml to dict:dictvalue
            # dictvalue example:
            # key: ('module', 'IP_conf', 'function', 'STATION_Setting', 'option', '0-0-11.MAC1')
            # value: '00:11:3f:ce:f3:4d'
        2. get hardware type, zone id, msgh number, NRG number etc.
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
        doc = lxml.etree.parse('SDM_General_Data_bono10.xml')
        print doc
        print doc.getroot().tag
        for firstlevel in doc.getroot():
            #print (firstlevel.tag, firstlevel.attrib)
            for secondlevel in firstlevel:
                secondlevelname = secondlevel.get('name')
                msgh = re.search(r'msgh(\d+)_Traffic_IPV4', secondlevelname)
                if msgh:
                    self.msghnumber.append(msgh.group(1))
                for thirdlevel in secondlevel:
                    #datapath = '//'+firstlevel.tag+'[@name="%s"]/'+secondlevel.tag+'[@name="%s"]/'+thirdlevel.tag+'[@name="%s"]/@value'
                    datapath = '//'+firstlevel.tag+'[@name="%s"]/'+secondlevel.tag+'[@name="%s"]/'+thirdlevel.tag+'[@name="%s"]'
                    datavalue = datapath+'/@value'
                    test = doc.xpath(datavalue %(firstlevel.get('name'), secondlevel.get('name'), thirdlevel.get('name')))
                    if firstlevel.get('name') == 'IP_conf' and secondlevel.get('name') == 'LDAP_Traffic_IPV4' and thirdlevel.get('name') == 'VLAN_ID':
                        print 'help:'+str(thirdlevel.get('version'))+'!'
                        thirdlevel.set('version', '2')
                        print 'help:'+str(thirdlevel.get('version'))+'!'
                    dictvalue[(firstlevel.tag, firstlevel.get('name'), secondlevel.tag, secondlevel.get('name'), thirdlevel.tag, thirdlevel.get('name'))] = thirdlevel.get('value')

        # 2. get hardware type, zone id, msgh number, NRG number etc.          
        self.hardwaretype = doc.xpath(datavalue %('General', 'Common', 'HARDWARE'))[0]
        print 'hardware type is: %s'%self.hardwaretype
        self.msghnumber.sort()
        print 'msgh number is: %s'%self.msghnumber[-1]
        
        # 3. generate new SDM_General_Data.xml based on result in step2 and new SDM_General_Data_template.xml
        
        # 4. parse new xml file into newdoc = lxml.etree.parse(newxml)
        newxml = 'SDM_General_Data.xml'
        newdoc = lxml.etree.parse(newxml)
        print newdoc.getroot()
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
        # 6. write to new SDM_General_Data-[lab name].xml file newdoc.write('SDM_General_Data-[lab name].xml')
        newdoc.write('bono10.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
        '''# write to new xmltree.xml file after update(set) value
        test = 'atca23'
        doc.write('xmltree-%s.xml'%test)
        '''
mergeToNewxml = MergeToNewxml()
mergeToNewxml.mergeFile()
        