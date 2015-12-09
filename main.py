'''
Created on Dec 9, 2015

@author: dadl
'''
import os
from lib.ssh import ssh_manager
import get_files
import get_filelist

class MyPractice(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

if __name__ == '__main__':
    myPractice = MyPractice()
    lab = 'atca55'
    remotedir = '/PLATsoftware/pt_result/2015-12-03/fm1945_'+lab+'/Done/'
    localdir = './rawdata/'
    '''
    #1. create SshManager instance
    '''
    ssh = ssh_manager.SshManager()
    #result = ssh.run('atca55', 'ls /root/GD_tool')
    '''
    2. scp files from lab(s)
    '''
    getfiles = get_files.GetFiles(ssh)
    files = getfiles.getFilesFromLab(lab, remotedir)
    '''
    #3. get ready to parse files list for each lab
    '''
    #1st method: use get_filelist
    #getfilelist = get_filelist.GetFileList()
    #filelist = getfilelist.getFileList(lab, localdir)
    #2nd method: directly use get_files return string
    for line in files:
        print line.split('/')[-1]
    '''
    #4. analyze/parse data to dictCpu
    '''
    
    '''
    #5. write data into excel(many sheets)/csv file(s) for each lab
    '''
    
    
            