'''
Created on 2015.12.13

@author: dadl
'''

class TestException(object):
    '''
    classdocs
    '''
    bar = 'spam'

    def __init__(self):
        '''
        Constructor
        '''
    def nameError(self):
        pass
    def ioError(self):
        try:
            f = open('blah', 'r')
            print 'test 1'
        except IOError, e:
            print 'cound not open file:', e
        
        print 'test 2'
        
    def safe_float(self, obj):
        try:
            retval = float(obj)
        except ValueError:
            retval = 'Could not convert non-number to float'
        except TypeError:
            retval = 'Input object is not a string or a number'
        return retval

    def safe_float2(self, obj):
        try:
            retval = float(obj)
        except (ValueError, TypeError), diag:
            retval = diag
        return retval
    
#     def testElse(self):
#         import 3rd_party_module
#         log = open('logfile.txt', 'w')
#         try:
#             3rd_party_module.function()
#         except:
#             log.write('*** caught exception in module\n')
#         else:
#             log.write('*** no exceptions caught\n')
#         log.close()        

testException = TestException()
result = testException.safe_float2({})

print result





        