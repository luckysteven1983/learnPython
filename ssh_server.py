'''
Created on Dec 24, 2015

@author: dadl
'''
import threading
from socket import *
from paramiko.transport import Transport
class SshServer(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    sock = ('', 8022)
    sshSerSock = socket(AF_INET, SOCK_STREAM)
    sshSerSock.bind(sock)
    sshSerSock.listen(5)
    
    transport = Transport(sshSerSock)
    print '1. waiting for connection...'
    transport.start_server()
    print '2. waiting for connection...'
    print transport.is_alive()
    
'''
        D:\workspace\PythonCase\src\Python27>netstat

Active Connections

  Proto  Local Address          Foreign Address        State
  TCP    127.0.0.1:54887        CV0037126N0:54888      ESTABLISHED
  TCP    127.0.0.1:54888        CV0037126N0:54887      ESTABLISHED
  TCP    127.0.0.1:54889        CV0037126N0:54890      ESTABLISHED
  TCP    127.0.0.1:54890        CV0037126N0:54889      ESTABLISHED
  TCP    127.0.0.1:56082        CV0037126N0:56083      ESTABLISHED
  TCP    127.0.0.1:56083        CV0037126N0:56082      ESTABLISHED
  TCP    127.0.0.1:56087        CV0037126N0:56088      ESTABLISHED
  TCP    127.0.0.1:56088        CV0037126N0:56087      ESTABLISHED
  TCP    127.0.0.1:58255        CV0037126N0:58256      ESTABLISHED
  TCP    127.0.0.1:58256        CV0037126N0:58255      ESTABLISHED
  TCP    127.0.0.1:58445        CV0037126N0:58446      ESTABLISHED
  TCP    127.0.0.1:58446        CV0037126N0:58445      ESTABLISHED
  TCP    127.0.0.1:58481        CV0037126N0:58482      ESTABLISHED
  TCP    127.0.0.1:58482        CV0037126N0:58481      ESTABLISHED
  TCP    127.0.0.1:63016        CV0037126N0:63017      ESTABLISHED
  TCP    127.0.0.1:63017        CV0037126N0:63016      ESTABLISHED
  TCP    127.0.0.1:63025        CV0037126N0:63026      ESTABLISHED
  TCP    127.0.0.1:63026        CV0037126N0:63025      ESTABLISHED
  TCP    127.0.0.1:63097        CV0037126N0:63158      ESTABLISHED
  TCP    127.0.0.1:63158        CV0037126N0:63097      ESTABLISHED
  TCP    127.0.0.1:63293        CV0037126N0:63318      ESTABLISHED
  TCP    127.0.0.1:63294        CV0037126N0:63315      ESTABLISHED
  TCP    127.0.0.1:63307        CV0037126N0:63321      ESTABLISHED
  TCP    127.0.0.1:63315        CV0037126N0:63294      ESTABLISHED
  TCP    127.0.0.1:63316        CV0037126N0:63317      ESTABLISHED
  TCP    127.0.0.1:63317        CV0037126N0:63316      ESTABLISHED
  TCP    127.0.0.1:63318        CV0037126N0:63293      ESTABLISHED
  TCP    127.0.0.1:63319        CV0037126N0:63320      ESTABLISHED
  TCP    127.0.0.1:63320        CV0037126N0:63319      ESTABLISHED
  TCP    127.0.0.1:63321        CV0037126N0:63307      ESTABLISHED
  TCP    127.0.0.1:63322        CV0037126N0:63323      ESTABLISHED
  TCP    127.0.0.1:63323        CV0037126N0:63322      ESTABLISHED
  TCP    127.0.0.1:63737        CV0037126N0:63739      ESTABLISHED
  TCP    127.0.0.1:63739        CV0037126N0:63737      ESTABLISHED
  TCP    135.252.158.247:49736  Imap:16651             ESTABLISHED
  TCP    135.252.158.247:57124  pcp048326pcs:5922      ESTABLISHED
  TCP    135.252.158.247:57320  bl1015:5920            ESTABLISHED
  TCP    135.252.158.247:58448  135.251.33.31:8080     ESTABLISHED
  TCP    135.252.158.247:62975  ngnac-bjwj:10003       ESTABLISHED
  TCP    135.252.158.247:63161  sippoolams0e04:https   ESTABLISHED
  TCP    135.252.158.247:63382  app:microsoft-ds       ESTABLISHED
  TCP    135.252.158.247:63477  Imap:7830              ESTABLISHED
  TCP    135.252.158.247:64614  Imap:7830              ESTABLISHED
  TCP    135.252.158.247:64615  Imap:7830              ESTABLISHED
  TCP    135.252.158.247:64624  CNSHJMBX03:7830        ESTABLISHED
  TCP    [2002:87fc:9ef7::87fc:9ef7]:49875  [2002:87fc:a621::87fc:a621]:52598  E
STABLISHED
  TCP    [2002:87fc:9ef7::87fc:9ef7]:63708  [2002:87fc:a610::87fc:a610]:10123  E
STABLISHED
'''