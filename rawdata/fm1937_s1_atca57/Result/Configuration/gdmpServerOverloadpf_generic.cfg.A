# 12-12-12 F.Veillon CR # DCTPD00861962 : ACOS #68965 : Not possible to install UDM2.0 on Bono hardware
# 15-12-14 Y.Kergus FFRD -192338 : DDM critical resource management enhancements (Feature 76314)


WORKING_DIRECTORY = /var/local/nectar/crash/GDMPCrash

NB_GDMP_SERVER_CORE_ALLOWED = 20

TRACE_FILE = "INT,0x3e:/var/local/nectar/log/gdmpServerOverload.log"
TRACE_ENABLE = YES

REMOTE_CONTROL_PORT             = 30114
BCKDLOG_FILE = "INT,0xff:/var/local/nectar/log/gdmpServerOverload_backdoor.log"

# Use sched inherit
GDMP_OVERLOAD_USE_SCHED_INHERIT = NO


# process size default 400 M
DHAFW_MAX_PROCESS_SIZE_MBYTES = 400
#GDMP_OVERLOAD_PROCESS_SIZE_MBYTES = 400

# process number max of threads 
DHAFW_MAX_PROCESS_THREADS_NUMBER = 100

# scheduler policy FIFO
GDMP_OVERLOAD_THREAD_POLICY = 1

# priority 33
GDMP_OVERLOAD_THREAD_PRIORITY = 33

# Stack size 48 k
GDMP_OVERLOAD_STACK_SIZE = 49152

# Type of monitored memory GDMP or STATION
MONITORED_MEMORY = GDMP 

# overlaod CPU treatment not inhibited
CPU_OVERLOAD_INHIBITED = NO

# overlaod MEM treatment not inhibited
MEM_OVERLOAD_INHIBITED = NO

# Audit period in ms
CPU_OVERLOAD_TIMER_RATE = 2000
MEM_OVERLOAD_TIMER_RATE = 2000

# Number of samples to consolidate the load
CPU_OVERLOAD_NEEDED_SAMPLES_NUMBER = 3
MEM_OVERLOAD_NEEDED_SAMPLES_NUMBER = 3

# Maximum CPU allowed in % (for example 100 for ROUZIC and less than 100 for BONO)
MAX_ALLOWED_CPU = 100

# Maximum Memory used in %
MAX_ALLOWED_MEM = 100

# CPU Thresholds defined in % of MAX_ALLOWED_CPU
CPU_G2_WARNING_LOW = 65
CPU_G2_WARNING_HIGH = 75
CPU_G2_REGULATION = 85

# CPU G3 Threshold is introduced but level load 4 (load > G3_REGULATION) is never set for CPU
CPU_G3_REGULATION = 95 

# MEM Thresholds defined in % of MAX_ALLOWED_MEM
MEM_G2_WARNING_LOW = 65
MEM_G2_WARNING_HIGH = 75
MEM_G2_REGULATION = 85
MEM_G3_REGULATION = 95

# CPU consolidate method is average
CPU_CONSOLIDATE_METHOD = 0

# MEM consolidate method is average
MEM_CONSOLIDATE_METHOD = 0


# Method to compute load for 24 CPU conf
# CPU_CPU24_LOAD_METHOD = 0    : like other conf CPU load total = user + system + nice + idle + ioait + irq + sirq + stolen + guest
# CPU_CPU24_LOAD_METHOD = 1    : specific CPU load total = user + system + nice + idle
CPU_CPU24_LOAD_METHOD = 0

# IOWAIT management in CPU LOAD comput 0 (10O% - IDLE - IOWAIT) 1 (100% - IDLE) 2 (100% - IDLE + IOWAIT) 
# Note on conf 24 CPU if CPU_CPU24_LOAD_METHOD = 0 automatically IOWAIT_IN_CPU_USAGE is treated as 1
IOWAIT_IN_CPU_USAGE = 0

# Supplementary CPU traces activation
CPU_SUPP_TRACE = 0

# Supplementary MEM trace activation
MEM_SUPP_TRACE = 0 

# send cpu load to smps
SEND_CPU_LOAD_TO_SMPS = yes

# send mem load to smps
SEND_MEM_LOAD_TO_SMPS = yes

# For SMPS connection
MATED_GMPS_PORT = 15777
MATED_GMPS_HOSTNAME = Pilot_Activ
SMPS_TIME_OUT_CONNECTION = 3000
CHECK_SMPS_CONNECTION_AUDIT = 1000

#DCTPD01024907
#AutoInitPfProxy=false
