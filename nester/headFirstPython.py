import sys
movies = ["holy grail", 1975, "Terry Jones", 91,
               ["Graham Chapman", ["Michael Palin", "John cleese",
                      "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

#print movies

'''
def print_lol(the_list, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for i in range(level):
                print "\t",
            print each_item
'''

def print_lol(the_list, indent=False, level=0, fn=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fn)
        else:
            if indent:
                for i in range(level):
                    print >> fn, "\t",
            print >> fn, each_item

#print_lol(movies, 2)
print_lol(movies)
print '###########'
print_lol(movies,True)
#print_lol(movies,1)
