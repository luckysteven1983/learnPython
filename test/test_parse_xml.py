'''
Created on Dec 10, 2015

@author: dadl
'''
import xml.dom.minidom
import lxml.etree

input_xml_string = """ 
                   <root> 
                        <item> 
                            <data version="1.0" url="http://***" /> 
                            <data version="2.0" url="http://***" /> 
                         </item> 
                         <other> 
                             <data version="1.0" url="http://***" /> 
                             <data version="2.0" url="http://***" /> 
                          </other> 
                     </root> 
                     """  


def get_tagname():
    doc = xml.dom.minidom.parseString(input_xml_string)
    for node in doc.getElementsByTagName("data"):
        print (node, node.tagName, node.getAttribute("version"))

def get_tagname_other():  
    doc = xml.dom.minidom.parseString(input_xml_string)  
    for node in doc.getElementsByTagName("data"):  
        if node.parentNode.tagName == "other":  
            print (node, node.tagName, node.getAttribute("version"))  
            

def get_xpath_2():  
    #doc = lxml.etree.XML(input_xml_string)
    doc = lxml.etree.parse('data.xml')
    doc.getroot()
    print doc.getroot()
    #for node in doc.xpath("//item/data[@version = $name]", name = "1.0"):  
    for node in doc.xpath("//item/data"): 
        print (node, node.tag, (node.items()))
    print doc.xpath("//item/data")

def test_parse_xml():
    dictvalue = {}
    doc = lxml.etree.parse('SDM_General_Data.xml')
    print doc.getroot().tag
    for firstlevel in doc.getroot():
        #print (firstlevel.tag, firstlevel.attrib)
        for secondlevel in firstlevel:
            for thirdlevel in secondlevel:
                #for datakey in thirdlevel.keys():
                    #print datakey
                    #print (firstlevel.tag, secondlevel.tag, thirdlevel.tag, datakey, thirdlevel.get(datakey))
                #print {(firstlevel.get('name'), secondlevel.get('name'), thirdlevel.get('name')) : thirdlevel.get('value')}
                #datapath = '//'+firstlevel.tag+'[@name="%s"]/'+secondlevel.tag+'[@name="%s"]/'+thirdlevel.tag+'[@name="%s"]/@value'
                datapath = '//'+firstlevel.tag+'[@name="%s"]/'+secondlevel.tag+'[@name="%s"]/'+thirdlevel.tag+'[@name="%s"]'
                datavalue = datapath+'/@value'
                test = doc.xpath(datavalue %(firstlevel.get('name'), secondlevel.get('name'), thirdlevel.get('name')))
                print (firstlevel.get('name'), secondlevel.get('name'), thirdlevel.get('name'), test)
                #dictvalue[(firstlevel.get('name'), secondlevel.get('name'), thirdlevel.get('name'))] = thirdlevel.get('value')
#     print node.get('name')
#     anotherkey = ('IP_conf', 'BE.NETWORK.NRG.1.ZONE.1_IPV6', 'GMPS.HOSTNAME', 'Private_VLAN1')
#     print '\n'
#     print 'another value of dictvalue is: '+dictvalue[anotherkey]+'!'

test_parse_xml()
#get_xpath_2()
