'''
Created on Dec 22, 2015

@author: dadl
'''
import pexpect

class TestPexpect(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
if __name__=='__main__':
    #testPexpect = TestPexpect()
    fout = open('log.txt', "wb")
    session = pexpect.spawn('ssh ainet@atca23')
    session.logfile = fout
    session.expect('.*ssword:')
    session.sendline('ainet1')
    session.expect('.*>')
    session.sendline('su - root')
    session.expect('.*ssword:')
    session.sendline('r00t')
    session.expect('.*#')
    session.send('ls /root\n')
    session.expect('.*#')
    fout.close()
    #session.interact()
    session.close()
    
        