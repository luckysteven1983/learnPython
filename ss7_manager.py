'''
Created on Nov 3, 2015

@author: xzhao015
'''

import re
from framework.testenv.frontend import Frontend
import lib.exceptions_messages as msgs
from lib.logging.logger import Logger
LOGGER = Logger.getLogger(__name__)

SS7_PROCESS_RESTART_TIMEOUT = 60
SS7_PROCESS_RESTART_CHECK_INTERVAL = 5
CMD_ASSOC_STATUS_ALL = "op:status,assoc=all;"
CMD_ASSOC_STATUS_M3UA = "op:status,assoc=all,m3ua;"
CMD_ASSOC_STATUS_M2PA = "op:slk=eqp;"
M3UA_TYPE = "M3UA"
M3UA_CLIENT = "M3UA CLIENT"
M2PA_CLIENT = "M2PA CLIENT"
M3UA_ESTABLISHED = "ESTABLISHED"
M2PA_ACTIVE = "ACTIVE"
SS7_NOT_CONFIGURED = "FAILED - NO ASSOCIATION IS EQUIPPED"
INVALID_RESPONSE_MESSAGE = "INVALID RESPONSE MESSAGE"

def getProcessNumber(lab, nodeNumber):
    '''
    according to the node number and SS7 Stacks Mode to get the S7SCH or STSCH process Number
    node number is the node value get from op:ss7master or op:sgmaster
    if SS7 Stacks Mode is "M", processNumber is nodeNumber%4
        nodeNumber is 7, processNumber is 3
    if SS7 Stacks Mode is "C", processNumber is ""

    @param lab: lab type
    @param nodeNumber: string, the node number
    '''
    processNumber = ""
    if lab.productRole.ss7StacksMode.upper() == "M":
        processNumber = str(int(nodeNumber) % 4)
    return processNumber

class SS7ManagerError(BaseException):
    """If error, raise it."""
    pass

class SS7Manager(object):
    '''
    SS7Manager is related to ss7 operation on lab.
    '''

    def __init__(self, sshManager, linuxProcessManager, subshlManager):
        '''
        Constructor
        '''
        self._sshManager = sshManager
        self._linuxProcessManager = linuxProcessManager
        self._subshl = subshlManager

    def _getMasterProcess(self, lab, processKeyWord):
        '''
        get Master S7SCH or STSCH

        @param lab: lab type
        @param processKeyWord: string only support "S7SCH" and "STSCH"
        @return: tuple (processName, machine)
        @author: Xia zhao

        @verbatim
        processName, machine = _getMasterProcess(self, lab, 'S7SCH')
        @endverbatim
        '''
        exceptionMessage = ""
        cmd = ""
        processNamePrefix = ""
        LOGGER.debug(lab.id + ": try to get master " + processKeyWord)
        if processKeyWord.upper() == 'S7SCH':
            exceptionMessage = lab.id + ": " + msgs.GET_MASTER_S7SCH_FAILED
            cmd = "op:ss7master;"
            processNamePrefix = "S7SCH"
        elif processKeyWord.upper() == 'STSCH':
            exceptionMessage = lab.id + ": " + msgs.GET_MASTER_STSCH_FAILED
            cmd = "op:sgmaster;"
            processNamePrefix = "STSCH"
        else:
            LOGGER.error(msgs.SS7_NOT_SUPPORTED_PROCESS)
            raise SS7ManagerError, msgs.SS7_NOT_SUPPORTED_PROCESS

        if not isinstance(lab.productRole, Frontend):
            LOGGER.error(msgs.SS7_NOT_SUPPORTED_LAB_TYPE)
            raise SS7ManagerError, msgs.SS7_NOT_SUPPORTED_LAB_TYPE

        try:
            ss7Info = self._subshl.run(lab, cmd)
        except:
            exceptionMessage += ": " + msgs.RUN_SUBSHL_CMD_FAILED
            LOGGER.error(exceptionMessage)
            raise SS7ManagerError, exceptionMessage

        node = ""
        machine = ""
        found = re.search(r'NODE=(\d+)', ss7Info)
        if found:
            node = found.group(1)
        ss7Info = "".join(ss7Info.splitlines()).replace(' ', '')
        found = re.search(r'-(\d+-\d+-\d+)\.', ss7Info)
        if found:
            machine = found.group(1)

        if not node or not machine:
            LOGGER.error(exceptionMessage)
            raise SS7ManagerError, exceptionMessage

        processNumber = getProcessNumber(lab, node)
        process = processNamePrefix + processNumber

        return process, machine

    def getMasterS7SCH(self, lab):
        '''
        get Master S7SCH
        < op:ss7master; PF
        +++ ATCA27 2015-11-04 10:54:26 MAINT /S7220 #009779 0-0-1 >
        M  OP SS7MASTER COMPLETED, MASTER S7SCH NODE=0 HOST=as006 MACHINE=ATCA27-0-0-6.
        END OF REPORT #009779++-

        @param lab: lab type
        @return: tuple (processName, machine)
                eg: S7SCH, 0-0-6
        @author: Xia zhao

        @verbatim
        processName, machine = getMasterS7SCH(lab)
        @endverbatim
        '''

        return self._getMasterProcess(lab, 'S7SCH')

    def getMasterSTSCH(self, lab):
        '''
        get Master STSCH
        < op:sgmaster; PF
        +++ BONO10 2015-11-05 10:37:46 MAINT /SG011 #140045 0-0-1 >
        M  OP SGMASTER COMPLETED, MASTER STSCH NODE=0 HOST=as002 MACHINE=BONO10-0-0-2.
        END OF REPORT #140045++-


        @param lab: lab type
        @return: tuple (processName, machine)
                eg: STSCH0, 0-0-2
        @author: Xia zhao

        @verbatim
        processName, machine = getMasterSTSCH(lab)
        @endverbatim
        '''
        return self._getMasterProcess(lab, 'STSCH')

    def _killMasterProcess(self, lab, processKeyWord):
        '''
        kill Master S7SCH/STSCH process

        @param lab: lab type
        @param processKeyWord: string only support "S7SCH" and "STSCH"
        @author: Xia zhao

        @verbatim
        _killMasterProcess(lab, 'S7SCH')
        @endverbatim
        '''
        exceptionMessage = ""
        LOGGER.debug(lab.id + ": try to kill master process" + processKeyWord)
        if processKeyWord.upper() == 'S7SCH':
            exceptionMessage = lab.id + ": " + msgs.KILL_MASTER_S7SCH_FAILED
        elif processKeyWord.upper() == 'STSCH':
            exceptionMessage = lab.id + ": " + msgs.KILL_MASTER_STSCH_FAILED
        else:
            LOGGER.error(msgs.SS7_NOT_SUPPORTED_PROCESS)
            raise SS7ManagerError, msgs.SS7_NOT_SUPPORTED_PROCESS

        try:
            processName, machine = self._getMasterProcess(lab, processKeyWord)
            self._linuxProcessManager.advancedKillWaitProcess(lab, processName, [machine],
                                                              SS7_PROCESS_RESTART_TIMEOUT,
                                                              SS7_PROCESS_RESTART_CHECK_INTERVAL,
                                                              'debug')
        except:
            LOGGER.error(exceptionMessage)
            raise SS7ManagerError, exceptionMessage

    def killMasterS7SCH(self, lab):
        '''
        kill Master S7SCH process

        @param lab: lab type
        @author: Xia zhao

        @verbatim
        killMasterS7SCH(lab)
        @endverbatim
        '''
        self._killMasterProcess(lab, 'S7SCH')

    def killMasterSTSCH(self, lab):
        '''
        kill Master STSCH process

        @param lab: lab type
        @author: Xia zhao

        @verbatim
        killMasterSTSCH(lab)
        @endverbatim
        '''
        self._killMasterProcess(lab, 'STSCH')


    def checkAssociationsEstablished(self, lab):
        """
        Checks that the SIGTRAN associations are established/active
        @param lab: front-end (Lab instance)
        @exception SS7ManagerError: raised if some links are not active
        @verbatim
        Output from "op:status,assoc=all,m3ua" (M3UA)
        1. Inactive links
                ASSOCIATION      STATUS    CONN STATUS     ASP STATUS    RSP STATUS
           ------------------  --------  -------------  -------------  -------------
            0-1  M3UA CLIENT        ACT           DOWN           DOWN             NA
            1-2  M3UA CLIENT        ACT           DOWN           DOWN             NA
            2-3  M3UA CLIENT        ACT           DOWN           DOWN             NA
            3-4  M3UA CLIENT        ACT           DOWN           DOWN             NA
            4-5  M3UA CLIENT        OOS           DOWN           DOWN             NA
            5-6  M3UA CLIENT        OOS           DOWN           DOWN             NA
            6-7  M3UA CLIENT        OOS           DOWN           DOWN             NA
            7-8  M3UA CLIENT        OOS           DOWN           DOWN             NA

        2. Active links
                ASSOCIATION      STATUS    CONN STATUS     ASP STATUS    RSP STATUS
           ------------------  --------  -------------  -------------  -------------
            0-1  M3UA CLIENT        ACT    ESTABLISHED         ACTIVE             NA
            1-2  M3UA CLIENT        ACT    ESTABLISHED         ACTIVE             NA
            2-3  M3UA CLIENT        ACT    ESTABLISHED         ACTIVE             NA
            3-4  M3UA CLIENT        ACT    ESTABLISHED         ACTIVE             NA
            4-5  M3UA CLIENT        OOS    ESTABLISHED           DOWN             NA
            5-6  M3UA CLIENT        OOS    ESTABLISHED           DOWN             NA
            6-7  M3UA CLIENT        OOS    ESTABLISHED           DOWN             NA
            7-8  M3UA CLIENT        OOS    ESTABLISHED           DOWN             NA


        Output from "op:slk=eqp" (M2PA)
        1. Inactive links
        +-----------------------------+----------------------+--------+-----------+
        |        LINK DATA            |     STATUS FLAGS     |  LINK  |    LINK   |
        +-----------------------------+----------------------+ACTIVITY|AVAILABILTY|
        |  No.   |LS|SLC|Cg|LFC|CLASS |FAIL|BLK|RBLK|INH|RINH|  STATE |    STATE  |
        +--------+--+---+--+---+------+----+---+----+---+----+--------+-----------+
        |   0-1-1| 1|  1| 0|SRE|M2PA  |  Y |   |    |   |    |ACT/REST|UNAVAILABLE|
        +--------+--+---+--+---+------+----+---+----+---+----+--------+-----------+
        |   1-1-1| 1|  2| 0|   |M2PA  |  Y |   |    |   |    |ACT/REST|UNAVAILABLE|
        +--------+--+---+--+---+------+----+---+----+---+----+--------+-----------+
        2. Active links
        +-----------------------------+----------------------+--------+-----------+
        |        LINK DATA            |     STATUS FLAGS     |  LINK  |    LINK   |
        +-----------------------------+----------------------+ACTIVITY|AVAILABILTY|
        |  No.   |LS|SLC|Cg|LFC|CLASS |FAIL|BLK|RBLK|INH|RINH|  STATE |    STATE  |
        +--------+--+---+--+---+------+----+---+----+---+----+--------+-----------+
        |   0-1-1| 1|  1| 0|SRE|M2PA  |    |   |    |   |    | ACTIVE | AVAILABLE |
        +--------+--+---+--+---+------+----+---+----+---+----+--------+-----------+
        |   1-1-1| 1|  2| 0|   |M2PA  |    |   |    |   |    | ACTIVE | AVAILABLE |
        +--------+--+---+--+---+------+----+---+----+---+----+--------+-----------+
        @endverbatim
        """

        assocsStatusAll = self._subshl.run(lab, CMD_ASSOC_STATUS_ALL)

        if assocsStatusAll.find(SS7_NOT_CONFIGURED) != -1:
            LOGGER.error(msgs.LINKS_NOT_ACTIVE)
            raise SS7ManagerError, msgs.LINKS_NOT_ACTIVE

        if assocsStatusAll.find(INVALID_RESPONSE_MESSAGE) != -1:
            errorMsg = msgs.LINKS_NOT_ACTIVE + ": " + INVALID_RESPONSE_MESSAGE
            LOGGER.error(errorMsg)
            raise SS7ManagerError, errorMsg

        if assocsStatusAll.find(M3UA_TYPE) != -1:
            # M3UA case
            assocsStatus = self._subshl.run(lab, CMD_ASSOC_STATUS_M3UA)
            assocsNb = assocsStatus.count(M3UA_CLIENT)
            activeAssocsNb = assocsStatus.count(M3UA_ESTABLISHED)
        else:
            # M2PA case
            assocsStatus = self._subshl.run(lab, CMD_ASSOC_STATUS_M2PA)
            assocsNb = assocsStatus.count(M2PA_CLIENT)
            activeAssocsNb = assocsStatus.count(M2PA_ACTIVE)

        if activeAssocsNb != assocsNb:
            LOGGER.error(msgs.LINKS_NOT_ACTIVE)
            raise SS7ManagerError, msgs.LINKS_NOT_ACTIVE

