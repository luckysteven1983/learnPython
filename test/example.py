#-------------------------------------------------------------------------------
# Author:      User
#
# Created:     31/08/2012
# Copyright:   (c) User 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#generated xml
#<?xml version="1.0" ?>
#<!--This is a simple xml.-->
#<books>
#     <book id="1001">
#         <title>
#         An apple
#         </title>
#     <author>
#         <name>
#             <firstname>
#             Peter
#             </firstname>
#             <lastname>
#             Zhang
#             </lastname>
#             </name>
#     </author>
#     <pubdate>
#     2012-1-12
#     </pubdate>
#     </book>
#
# .................
#</books>
from xml.dom import minidom, Node

class BooksXmlGenerator:
    def __init__(self):
        self.__doc = minidom.Document()
        self.__doc.appendChild(self.__doc.createComment("This is a sample xml"))
        self.__books = self.__doc.createElement("books")
        #self.__books.appendChild(self.__doc.createElement('book'))
        self.__doc.appendChild(self.__books)
        self.__booksSource = []

    def SetBooksSource(self, booksSource):
        for source in booksSource:
            self.__booksSource.append(source)


    def GenerateBooksXml(self):
        for newBook in self.__booksSource:
            book = self.__doc.createElement("book")
            book.setAttribute("id", newBook["id"])

            title = self.__doc.createElement("title")
            title.appendChild(self.__doc.createTextNode(newBook["title"]))
            book.appendChild(title)

            author = self.__doc.createElement("author")
            name = self.__doc.createElement("name")

            firstName = self.__doc.createElement("firstname")
            firstName.appendChild(self.__doc.createTextNode(newBook["firstname"]))

            lastName = self.__doc.createElement("lastname")
            lastName.appendChild(self.__doc.createTextNode(newBook["lastname"]))

            name.appendChild(firstName)
            name.appendChild(lastName)
            author.appendChild(name)
            book.appendChild(author)

            pubdate = self.__doc.createElement("pubdate")
            pubdate.appendChild(self.__doc.createTextNode(newBook["pubdate"]))
            book.appendChild(pubdate)

            self.__books.appendChild(book)

    def WriteToFile(self, path):
        f = file(path,"w")
        #self.__doc.writexml(f)
        self.__doc.writexml(f, addindent='    ', newl='\n',encoding='utf-8')
        f.close()

class BooksXmlScanner:
    def __init__(self, path):
        
        
        
        
        self.__doc = minidom.parse(path)
        for child in self.__doc.childNodes:
            if child.nodeType ==Node.COMMENT_NODE:
                print "Conment : " , child.nodeValue
            if child.nodeType == Node.ELEMENT_NODE:
                self.__HandleBooks(child)

    def __HandleBooks(self, node):
        for child in node.childNodes:
            if child.nodeType == Node.ELEMENT_NODE and child.tagName =="book":
                bookid = child.getAttribute("id")
                print "*"*20
                print "Book id : " , bookid
                self.__HandleBook(child)

    def __HandleBook(self, node):
        for child in node.childNodes:
            if child.nodeType ==Node.ELEMENT_NODE:
                if child.tagName == "title":
                    print "Title : " , self.__GetText(child.firstChild)
                if child.tagName == "author":
                    self.__HandleAuthor(child)
                if child.tagName == "pubdate":
                    print "Pubdate : " , self.__GetText(child.firstChild)

    def __GetText(self, node):
        if node.nodeType ==Node.TEXT_NODE:
            return node.nodeValue
        else:
            return ""

    def __HandleAuthor(self,node):
        author = node.firstChild
        for child in author.childNodes:
            if child.nodeType == Node.ELEMENT_NODE:
                if child.tagName == "firstname" :
                    print "Firstname : ", self.__GetText(child.firstChild)
                if child.tagName == "lastname" :
                    print "Lastname : " , self.__GetText(child.firstChild)

def main():
    path ="books.xml"
    booksGenerator = BooksXmlGenerator()
    sourceList =[{"id":"1002","title":"Love","firstname":"Mike","lastname":"Li","pubdate":"2012-1-10"},{"id":"1004","title":"Harry Potter","firstname":"Peter","lastname":"Chen","pubdate":"2012-11-11"},{"id":"1003","title":"Steve.Jobs","firstname":"Tom","lastname":"Wang","pubdate":"2012-1-19"}]
    booksGenerator.SetBooksSource(sourceList)
    booksGenerator.GenerateBooksXml()
    booksGenerator.WriteToFile(path)
    print "Write to file completely."

    #booksXmlScanner = BooksXmlScanner(path)

if __name__ == '__main__':
    main()