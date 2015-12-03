NDB_POLL_NB                    =  2048 
GDMI_TRANSACTIONS_PER_NDB       = 10    
MinReplyThreads = 16
NbReplyThreads = 250 
DHAFW_MAX_PROCESS_SIZE_MBYTES = 700
DHAFW_MAX_PROCESS_SIZE_HIGH_PERCENT = 75

#------------------------------------------------------------------------------#
#                        launch GdmpServer Configuration                       #
#------------------------------------------------------------------------------#
# default values:
#    - Nb GdmpServer core dump is limited to 2 (the oldest and the newest core)
#    - Core can be created if the file system percentage used is less than 75%

GDMP_CORE_LOCATION = "/var/local/nectar/crash/GdmpCrash"
NB_GDMP_SERVER_CORE_ALLOWED = 4
OLDEST_GDMP_SERVER_CORE_KEPT = 1
GDMP_PARTITION_SIZE_USED_THRESHOLD = 75
ClonePoolMaxSize = 64

ServerTcpNoDelay = true
# ServerSndBuf = 128000
# ServerRcvBuf = 128000

TriggerDisable = true
BCKDLOG_FILE = "INT,0xff:/var/local/nectar/out/backdoor_GdmpServer.log"

DisableShared = true
MaxGdmpMessageLength = 500000

TRACE_SYSLOG_MSGCLS=DDM

#DCTPD01024907
AutoInitPfProxy=false

#DCTPD01130394
ReplicationLoadUnmaskable = true

# DCTPD01066447: Alarm display persistence for several minutes after the end of the overload level 3/level 4
TEMPORIZED_ALARM_DELAY=30
TEMPORIZED_ALARMS_LIST="500 501 502 503"
