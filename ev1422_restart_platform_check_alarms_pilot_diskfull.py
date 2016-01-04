'''
Created on Dec 28, 2015
weblink_id:
@author: dadl
'''
from time import sleep
import random
from lib.logging.logger import Logger
from framework.asserts.common_asserts import CommonAssert
from lib.platform.mcas.mcas_platform_manager import MCAS_RESTART_PF_TIMEOUT
from lib.health_check.health_check_manager import HEALTH_CHECK_ASSERT_TIME_INTERVAL
from framework.sdm_test_case import SDMTestCase
from lib.alarm.alarms_config import AlarmsConfig
from lib.alarm.alarm import Alarm
from framework.common import Utils

LOGGER = Logger.getLogger(__name__)
LOGFILE = Logger.getAlarmLogFileNames(__name__)

class ev1422_restart_platform_check_alarms_pilot_diskfull(SDMTestCase):
    '''
    Pilot Disk is full, check the traffic impact; /etc/Astop all; /etc/Astart all; check the platform can be startup
    '''
    def setUp(self):
        self.logLinksPrint()
        self.mcasMachineManager = self.sdmManager.mcasMachineManager
        self.mcasPlatformManager = self.sdmManager.mcasPlatformManager
        self.allFEs = self.testEnv.testBed.getFrontends().values()
        self.fe = random.choice(self.allFEs)
        self.sshManager = self.sdmManager.sshManager
        self.testEnvAsserts = self.sdmManager.testEnvAsserts
        self.expectedAlarms = [Alarm(951205, "Major")]
        self.acceptedAlarms = []
        self.success = True
        self.exceptMsg = ""

    def test_restart_platform_check_alarms_pilot_diskfull(self):
        '''
        Procedure:
        1. Increase current partition on pilot to full
        2. restart platform by Astop/Astart all
        3. check alarm
        '''
        #-------------- Test case pre-check --------------
        LOGGER.debug("Check the Initial status of the test env")
        self.testEnvAsserts.assertInitialState(self.testEnv, LOGFILE[0])
        startTime = Utils.getCurrentLabTime(self.sdmManager.sshManager, self.allFEs[0])
        #-------------- Test case execution --------------
        LOGGER.info("Increase / partition to full by creating dummy file")
        cmd = 'dd if=/dev/zero of=/sncore/tmp.temp'
        self.sshManager.run(self.fe.oamIpAddress, cmd)
        LOGGER.info("%s: restart platform by Astop/Astart all", self.fe.id)
        self.mcasPlatformManager.runAstopAll(self.fe)
        self.mcasPlatformManager.runAstartAll(self.fe)
        LOGGER.info("Now waiting for SPAs to be recovered (max %s s)", MCAS_RESTART_PF_TIMEOUT)
        CommonAssert.timedAssert(MCAS_RESTART_PF_TIMEOUT, HEALTH_CHECK_ASSERT_TIME_INTERVAL,
                                 self.sdmManager.healthCheckManager.runCheckAll,
                                 self.fe, logLevel="debug")
        #-------------- Test case post-check --------------
        sleep(300)
        LOGGER.info("Restart traffics if needed")
        self.sdmManager.trafficManager.startTrafficsAgainIfNeeded()
        try:
            LOGGER.debug("Check the alarms")
            myAlarmsConfig = AlarmsConfig(self.expectedAlarms, self.acceptedAlarms, startTime)
            # Compares alarms from snmp log file to expected and accepted lists
            # but doesn't check all raised alarms are cleared
            self.sdmManager.alarmsCheckerManager.parseSnmpLogFiles(self.fe, myAlarmsConfig, logFile=LOGFILE[1])
        except BaseException, msg:
            # Verdict not yet based on alarms
            self.success = False
            self.exceptMsg += str(msg)
            LOGGER.error("%s: alarm check fail", self.fe.id)
        LOGGER.debug("Check the end status of the test env")
        try:
            labs = [lab for lab in self.testEnv.testBed.labs.values() if lab is self.fe]
            self.testEnvAsserts.assertEndState(self.testEnv, startTime, LOGFILE[2], checkNoPilotSwitchoverOnLabs=labs)
        except BaseException, msg:
            self.success = False
            self.exceptMsg += str(msg)
            LOGGER.error("%s: end state of test env check fail", self.fe.id)

        if self.success:
            LOGGER.debug("%s success!\n", self.__class__.__name__)
        else:
            LOGGER.error("%s failed!\n", self.__class__.__name__)
            LOGGER.error(self.exceptMsg)
            raise Exception(self.exceptMsg)

    def tearDown(self):
        '''
        Remove dummy file which is created during testcase execution
        '''
        LOGGER.debug("Clean dummy file")
        cmd = 'rm -f /sncore/tmp.temp'
        self.sshManager.run(self.fe.oamIpAddress, cmd, station='A')
        self.sshManager.run(self.fe.oamIpAddress, cmd, station='B')
