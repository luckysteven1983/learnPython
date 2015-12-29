'''
Created on Dec 28, 2015
weblink_id:
@author: dadl
'''
import random
from lib.logging.logger import Logger
from framework.sdm_test_case import SDMTestCase
from lib.alarm.alarms_config import AlarmsConfig
from framework.common import Utils

LOGGER = Logger.getLogger(__name__)
LOGFILE = Logger.getAlarmLogFileNames(__name__)

class ev1423_check_alarms_when_diskfull(SDMTestCase):
    '''
    Nonpilot Disk is full, check the alarm
    '''
    def setUp(self):
        self.logLinksPrint()  # Used to get the log links in Junit XML results
        self.myDSM = self.sdmManager.databaseStateManager
        self.mcasMachineManager = self.sdmManager.mcasMachineManager
        self.allFEs = self.testEnv.testBed.getFrontends().values()
        self.fe = random.choice(self.allFEs)
        self.stationList = self.fe.getStationListbyProductRole('RT').values()
        self.stationChosen = random.choice(self.stationList)
        self.sshManager = self.sdmManager.sshManager
        self.testEnvAsserts = self.sdmManager.testEnvAsserts
        self.expectedAlarms = []
        self.acceptedAlarms = []
        self.success = True
        self.exceptMsg = ""

    def test_check_alarms_when_diskfull(self):
        '''
        Procedure:
        1. Increase /sncore partition to full
        2. check alarm
        '''
        #-------------- Test case pre-check --------------
        LOGGER.debug("Check the Initial status of the test env")
        self.testEnvAsserts.assertInitialState(self.testEnv, LOGFILE[0])
        startTime = Utils.getCurrentLabTime(self.sdmManager.sshManager, self.allFEs[0])
        #-------------- Test case execution --------------
        LOGGER.debug("Increase /sncore partition to full by creating dummy file")
        cmd = 'cd /sncore;dd if=/dev/zero of=tmp.temp'
        self.sshManager.run(self.fe.oamIpAddress, cmd, station=self.stationChosen)
        #-------------- Test case post-check --------------
        try:
            LOGGER.debug("Check the alarms")
            myAlarmsConfig = AlarmsConfig(self.expectedAlarms, self.acceptedAlarms, startTime)
            # Compares alarms from snmp log file to expected and accepted lists
            # but doesn't check all raised alarms are cleared
            self.sdmManager.alarmsCheckerManager.parseSnmpLogFiles(self.fe, myAlarmsConfig, logFile=LOGFILE[1])
        except BaseException, msg:
            # Verdict not yet based on alarms
            self.exceptMsg += str(msg)
            LOGGER.error("%s: alarm check fail", self.fe)
            
        LOGGER.debug("Check the end status of the test env")
        try:
            labs = [lab for lab in self.testEnv.testBed.labs.values() if lab in self.fe]
            self.testEnvAsserts.assertEndState(self.testEnv, startTime, LOGFILE[2], checkNoPilotSwitchoverOnLabs=labs)
        except BaseException, msg:
            self.success = False
            self.exceptMsg += str(msg)
            LOGGER.error("%s: end state of test env check fail", self.fe.id)
        LOGGER.debug("%s success!\n", self.__class__.__name__)

    def tearDown(self):
        '''
        Remove dummy file which is created during testcase execution
        '''
        LOGGER.debug("Clean dummy file")
        cmd = 'cd /root;rm -f tmp.temp'
        self.sshManager.run(self.fe.oamIpAddress, cmd)