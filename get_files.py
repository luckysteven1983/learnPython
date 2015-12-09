'''
Created on Dec 9, 2015

@author: dadl
'''
import sys
class GetFiles(object):
    '''
    classdocs
    '''


    def __init__(self, ssh):
        '''
        Constructor
        '''
        self.ssh = ssh
    def getFilesFromLab(self, lab, remotedir):
        '''
        get files from lab       
        '''
        #ssh = ssh_manager.SshManager()
        iffile = self.ssh.run(lab, 'ls '+remotedir+'/top_*.log')
        #print iffile
        if iffile[0] == 0:
            fileList = self.ssh.scpGetAll(lab, remotedir+'/top_*.log')
        else:
            print 'Folder:%s does not contain top files for parsing!'%remotedir
            sys.exit()
        return fileList