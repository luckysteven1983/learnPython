#!/usr/bin/env python
# -*- coding: cp936 -*-
import os
from lib.ssh import ssh_manager

class RunCommand(object):
    def __init__(self, sshManager):
        self.sshManager = sshManager
    
    def runCmd(self, lab, command):
        #ssh = ssh_manager.SshManager()
        result = self.sshManager.run(lab, command)
        return result
           
# runCommand = RunCommand()
# result = runCommand.runCmd('atca55', 'ls /root/GD_tool')
# print result[0]
# print result[1].split('\n')