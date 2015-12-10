'''
Created on Dec 10, 2015

@author: dadl
#e.g. http://www.cnblogs.com/itech/archive/2011/01/06/1924972.html
'''
import os
class ParseXml(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def TestMiniDom(self):
        from xml.dom import minidom
        doc = minidom.parse("employees.xml")
        
        # get root element: <employees/>
        root = doc.documentElement
        
        # get all children elements: <employee/> <employee/>
        employees = root.getElementsByTagName("employee")
        
        for employee in employees:
            print("-------------------------------------------")
            # element name : employee
            print (employee.nodeName)
            # element xml content : <employee><name>windows</name><age>20</age></employee>
            # basically equal to toprettyxml function
            print (employee.toxml())
            
            nameNode = employee.getElementsByTagName("name")[0]
            print (nameNode.childNodes)
            print (nameNode.nodeName + ":" + nameNode.childNodes[0].nodeValue)
            ageNode = employee.getElementsByTagName("age")[0]
            print (ageNode.childNodes)
            print (ageNode.nodeName + ":" + ageNode.childNodes[0].nodeValue)
            
            print("-------------------------------------------")
            # children nodes :  \n is one text element
            # [
            # <DOM Text node "' \n    '">, 
            # <DOM Element: name at 0xc9e490>, 
            # <DOM Text node "'\n    '">, 
            # <DOM Element: age at 0xc9e4f0>, 
            # <DOM Text node "'\n  '">
            # ] 
            for n in employee.childNodes:
                print (n)

    def GenerateXml(self):
        import xml.dom.minidom
        impl = xml.dom.minidom.getDOMImplementation()
        dom = impl.createDocument(None, 'employees', None)
        root = dom.documentElement  
        employee = dom.createElement('employee')
        root.appendChild(employee)
        
        nameE=dom.createElement('name')
        nameT=dom.createTextNode('linux')
        nameE.appendChild(nameT)
        employee.appendChild(nameE)
        
        ageE=dom.createElement('age')
        ageT=dom.createTextNode('30')
        ageE.appendChild(ageT)
        employee.appendChild(ageE)
        
        
        f = open('employees2.xml', 'w')
        dom.writexml(f, addindent='  ', newl='\n',encoding='utf-8')
        f.close()  
        

parsexml = ParseXml()
#parsexml.TestMiniDom()            
parsexml.GenerateXml()






       