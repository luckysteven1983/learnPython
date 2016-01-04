'''
Created on Jan 6, 2016

@author: dadl
'''
from time import sleep
import random
from lib.logging.logger import Logger
from framework.sdm_test_case import SDMTestCase
from framework.common import Utils

LOGGER = Logger.getLogger(__name__)
LOGFILE = Logger.getAlarmLogFileNames(__name__)

class fr_SDM_10333(SDMTestCase):
    '''
    Pilot swo 10 times on FE and BE
    '''
    def setUp(self):
        self.logLinksPrint()  # Used to get the log links in Junit XML results
        self.databaseManager = self.sdmManager.databaseManager
        self.databaseStateManager = self.sdmManager.databaseStateManager
        self.mcasMachineManager = self.sdmManager.mcasMachineManager
        self.allBEs = self.testEnv.testBed.getBackends().values()
        self.be = random.choice(self.allBEs)
        self.allFEs = self.testEnv.testBed.getFrontends().values()
        self.fe = random.choice(self.allFEs)
        self.testEnvAsserts = self.sdmManager.testEnvAsserts
        self.expectedAlarms = []
        self.acceptedAlarms = []
        self.success = True
        self.exceptMsg = ""

    def test_SDM_10333(self):
        '''
        Procedure:
        Pilot swo 10 times on FE and BE
        '''
        #-------------- Test case pre-check --------------
        LOGGER.debug("Check the Initial status of the test env")
        self.testEnvAsserts.assertInitialState(self.testEnv, LOGFILE[0])
        startTime = Utils.getCurrentLabTime(self.sdmManager.sshManager, self.allBEs[0])
        #-------------- Test case execution --------------
        loop = 10
        LOGGER.info("Switch over FE and BE pilot %s times", loop)
        for i in range(loop):
            LOGGER.debug("%s: fe swo starts", self.fe.id)
            feSwoResult = self.mcasMachineManager.pilotSwitchover(self.fe)
            if not feSwoResult:
                self.success = False
            LOGGER.debug("%s: fe swo ends", self.fe.id)
        #Sleep 2 mins before continuing to do BE pilot swo
        sleep(120)
        for i in range(loop):
            LOGGER.debug("%s: be swo starts", self.be.id)
            beSwoResult = self.mcasMachineManager.pilotSwitchover(self.be)
            if not beSwoResult:
                self.success = False
            LOGGER.debug("%s: be swo ends", self.be.id)
        #-------------- Test case post-check --------------
        LOGGER.debug("Check the end status of the test env")
        try:
            labs = [lab for lab in self.testEnv.testBed.labs.values() if lab not in (self.fe, self.be)]
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
