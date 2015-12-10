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
    lxml.etree.parse('data.xml')
    doc = lxml.etree.ElementTree.__getattribute__()
    doc.getroot()
    for node in doc.xpath("//item/data[@version = $name]", name = "1.0"):  
        print (node, node.tag, (node.items()))
    print doc.xpath
                       

get_xpath_2()
