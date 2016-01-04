'''
Created on Jan 4, 2016

@author: dadl
'''
from lib.logging.logger import Logger
from framework.sdm_test_case import SDMTestCase
from framework.common import Utils

LOGGER = Logger.getLogger(__name__)
LOGFILE = Logger.getAlarmLogFileNames(__name__)

class fr_SDM_7910(SDMTestCase):
    '''
    Switch over Master NRG 100+ times
    '''
    def setUp(self):
        self.logLinksPrint()  # Used to get the log links in Junit XML results
        self.databaseManager = self.sdmManager.databaseManager
        self.databaseStateManager = self.sdmManager.databaseStateManager
        self.allBEs = self.testEnv.testBed.getBackends().values()
        self.beNrg1 = self.testEnv.testBed.getLabsInNRG()
        self.testEnvAsserts = self.sdmManager.testEnvAsserts
        self.expectedAlarms = []
        self.acceptedAlarms = []
        self.success = True
        self.exceptMsg = ""

    def test_SDM_7910(self):
        '''
        Procedure:
        Switch over Master NRG 100+ times
        '''
        #-------------- Test case pre-check --------------
        LOGGER.debug("Check the Initial status of the test env")
        self.testEnvAsserts.assertInitialState(self.testEnv, LOGFILE[0])
        startTime = Utils.getCurrentLabTime(self.sdmManager.sshManager, self.allBEs[0])
        #-------------- Test case execution --------------
        loop = 100
        LOGGER.info("Switch over Master NRG %s times", loop)
        for i in range(loop):
            beStates = dict((beObj.id, self.databaseStateManager.getState(beObj)) for beObj in self.beNrg1)
            LOGGER.debug("BE states before: %s", str(beStates))
            self.databaseManager.matedPairSwo(self.beNrg1)
            # Here we need to make sure the other BE status haven't changed
            newStates = dict((beObj.id, self.databaseStateManager.getState(beObj)) for beObj in self.beNrg1)
            LOGGER.debug("BE states after: %s", str(newStates))
            self.assertEqual(beStates.values().sort(), newStates.values().sort(), "Other BE states have changed!")
        #-------------- Test case post-check --------------
        LOGGER.debug("Check the end status of the test env")
        try:
            labs = [lab for lab in self.testEnv.testBed.labs.values() if lab is self.beNrg1]
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
