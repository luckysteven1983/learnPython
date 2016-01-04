'''
Created on Jan 4, 2016

@author: dadl
'''
from time import sleep
from lib.logging.logger import Logger
from framework.sdm_test_case import SDMTestCase
from lib.alarm.alarms_config import AlarmsConfig
from lib.platform.mcas.mcas_application_manager import SDM_SPA
from framework.common import Utils

LOGGER = Logger.getLogger(__name__)
LOGFILE = Logger.getAlarmLogFileNames(__name__)

class fr_SDM_10228(SDMTestCase):
    '''
    Restart the SPA about 60+ times in case of 1 PDLSU+3PDLSM
    '''
    def setUp(self):
        self.logLinksPrint()  # Used to get the log links in Junit XML results
        self.myDSM = self.sdmManager.databaseStateManager
        self.mcasMachineManager = self.sdmManager.mcasMachineManager
        self.mcasApplicationManager = self.sdmManager.mcasApplicationManager
        self.allFEs = self.testEnv.testBed.getFrontends().values()
        self.fe = self.allFEs[0]
        self.sshManager = self.sdmManager.sshManager
        self.testEnvAsserts = self.sdmManager.testEnvAsserts
        self.expectedAlarms = []
        self.acceptedAlarms = []
        self.success = True
        self.exceptMsg = ""

    def test_SDM_10228(self):
        '''
        Procedure:
        Restart SDM spa 60+ times
        '''
        #-------------- Test case pre-check --------------
        LOGGER.debug("Check the Initial status of the test env")
        self.testEnvAsserts.assertInitialState(self.testEnv, LOGFILE[0])
        startTime = Utils.getCurrentLabTime(self.sdmManager.sshManager, self.allFEs[0])
        #-------------- Test case execution --------------
        loop = 65
        LOGGER.info("Restarting SDM SPA %s times on %s", loop, self.fe.id)
        for i in range(loop):
            self.mcasApplicationManager.restartSPA(self.fe, SDM_SPA)
        #-------------- Test case post-check --------------
        #sleep(300)
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
