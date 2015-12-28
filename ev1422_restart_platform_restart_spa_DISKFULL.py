'''
Created on Dec 28, 2015

@author: dadl
'''
from lib.logging.logger import Logger
from framework.sdm_test_case import SDMTestCase
from lib.alarm.alarms_config import AlarmsConfig
from framework.common import Utils
import lib.exceptions_messages as msgs

LOGGER = Logger.getLogger(__name__)
LOGFILE = Logger.getAlarmLogFileNames(__name__)

class ev1422_restart_platform_restart_spa_DISKFULL(object):
    '''
    Pilot Disk is full, check the traffic impact; /etc/Astop all; /etc/Astart all; check the platform can be startup
    '''


    def setUp(self):
        self.logLinksPrint()
        self.myDSM = self.sdmManager.databaseStateManager
        self.mcasMachineManager = self.sdmManager.mcasMachineManager
        self.testEnvAsserts = self.sdmManager.testEnvAsserts
        self.expectedAlarms = []
        self.acceptedAlarms = []
        self.success = True
        self.exceptMsg = ""

    def test_restart_platform_restart_spa_DISKFULL(self):
        '''
        Procedure:
        1. Increase current partition to full (may implement it as a class)
        2. start traffic
        3. restart platform by Astop/Astart all
        4. check alarm
        5. restart SPA
        6. Check ...
        7. Recover lab by removing dummy file(s) which is/are created in step1
        '''
        #create dummy file to increase disk to full
        #1. increase current partition to full
        #   dd if=/dev/zero of=tmp.1G
        #2. create specific file size(512M*2=1024M=1G)
        #   dd if=/dev/zero of=tmp.1G bs=512M count=2
        
        
       
    def tearDown(self):
        pass
    
    
    def _increaseDiskUsage(self):
        pass 