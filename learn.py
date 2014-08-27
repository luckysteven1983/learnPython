from xml.dom.minidom import *
domfile=parse("System.xml")
root=domfile.documentElement
#children=root.childNodes
#print children
print root.nodeName,root.nodeValue,root.nodeType
db_nodes = root.getElementsByTagName("Database")
for node in db_nodes:
    node_addr = node.getElementsByTagName("Addr")	
    addr = node_addr[0].childNodes[0].nodeValue
    node_port = node.getElementsByTagName("Port")
    port = node_port[0].childNodes[0].nodeValue
    print 'IP Address:%s\nPort:%s'%(addr,port)
	
#node = root.getElementsByTagName("Addr")
#print node[0].childNodes[0].nodeValue
#print node.nodeName,node.nodeValue,node.nodeType
#print node.data
#print node[0].childNodes[0].nodeValue

sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print sum

sum1 = 0
m = 1
while m < 100:
    sum1 = sum1 + m
    m = m + 2
print sum1
