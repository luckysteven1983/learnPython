#!/bin/bash
awk 'BEGIN { printf "%-7s\t%-10s\t%-11s\t%-10s\n", "Station", "HottestCpu", "HottestCore", "AvgCoreCpu" }' > oam_cpu.report
for sta in A B
do
    ls -lrt |grep top_$sta > /dev/null
    if [ $? -eq 0 ]; then
		top_file=`ls -lrt top_$sta*|tail -1|awk '{print $9}'`
		#Number of CPU cores
		core_num=`cat /proc/cpuinfo|grep processor|wc -l`
		cmd="paste"
		for core in `seq $core_num`
		do
   			core=`expr $core - 1`
  			grep "Cpu${core} " $top_file | awk -F, '{ print $4 $5}'|sed -n -e 's/%id//p'|sed -n -e 's/%wa//p' | awk '{ printf "%.1f\n", 100-$1-$2}' > Cpu${core}
   			cmd=`echo $cmd " " Cpu${core}`
            #Calculate average/min/max CPU usage of each core
            awk '{ if(min=="") {min=max=$1}; if($1>max) {max=$1}; if($1< min) {min=$1}; total+=$1; count+=1} END {printf "%s\t%s\t%.1f\t%.1f\t%.1f\n", "'"$sta"'", "'"$core"'", total/count, min, max}' Cpu${core} >> Sta_${sta}_cpu.rpt
		done

		exec $cmd > cpu_$sta.txt &
		sleep 1
        #Calculate max CPU usage of each sample interval for station X
	max=`awk '{ max=0; for(i=1;i<=NF;i++) if(max<$i) max=$i; sum+=max; ++num; next } END {printf "%.1f", sum/num}' cpu_$sta.txt`
        hottestCore=`sort -n -k3 Sta_${sta}_cpu.rpt |tail -1|awk '{print $2}'`
        AvgCoreCpu=`sort -n -k3 Sta_${sta}_cpu.rpt |tail -1|awk '{print $3}'`
        awk 'BEGIN { printf "%-7s\t%-9.1f\t%-11d\t%-9.1f\n", "'"$sta"'", "'"$max"'", "'"$hottestCore"'", "'"$AvgCoreCpu"'" }' >> oam_cpu.report
        rm cpu_$sta.txt  Cpu*
    fi
done


sort -n -k2 oam_cpu.report|tail -1 |awk 'BEGIN { printf "%11s\t%11s\n", "OAM_MAX_CPU", "OAM_AVG_CPU" } { printf "%-10.1f\t%-10.1f\n", $2, $4} ' > oam_cpu.summary


for sta in `cat /etc/hosts|grep -i station|awk '{print $2}'|awk '{ gsub("STATION_","",$0); print;}'|grep -v [AB]|sort`
do
        #In case there are more than one top file for one station, we use the latest one.
        #top_file=`ls -lrt|grep top_${sta}|tail -1|awk '{print $9}'|wc -l`
        #In case there is no top file for some station, we ignore it.
        ls -lrt |grep top_$sta > /dev/null
        if [ $? -eq 0 ]; then
            top_file=`ls -lrt|grep top_${sta}|tail -1|awk '{print $9}'`
            core_num=`cat /proc/cpuinfo|grep processor|wc -l`
            cmd="paste"
            for core in `seq $core_num`
              do
                 core=`expr $core - 1`
                 grep "Cpu${core} " $top_file | awk -F, '{ print $4 $5}'|sed -n -e 's/%id//p'|sed -n -e 's/%wa//p' | awk '{ printf "%.1f\n", 100-$1-$2}' > Cpu${core}
                 cmd=`echo $cmd " " Cpu${core}`
				 #Calculate average/min/max CPU usage of each core
                 awk '{ if(min=="") {min=max=$1}; if($1>max) {max=$1}; if($1< min) {min=$1}; total+=$1; count+=1} END {printf "%s\t%s\t%.1f\t%.1f\t%.1f\n", "'"$sta"'", "'"$core"'", total/count, min, max}' Cpu${core} >> Sta_${sta}_cpu.rpt
              done

              exec $cmd > cpu_$sta.txt &
              sleep 1
              max=`awk '{ max=0; for(i=1;i<=NF;i++) if(max<$i) max=$i; sum+=max; ++num; next } END {printf "%.1f", sum/num}' cpu_$sta.txt`
              hottestCore=`sort -n -k3 Sta_${sta}_cpu.rpt |tail -1|awk '{print $2}'`
              AvgCoreCpu=`sort -n -k3 Sta_${sta}_cpu.rpt |tail -1|awk '{print $3}'`
#              echo -e $sta "\t" $max "\t" $hottestCore "\t" $AvgCoreCpu >> nonpilot_cpu.report 
        awk 'BEGIN { printf "%-7s\t%-9.1f\t%-11d\t%-9.1f\n", "'"$sta"'", "'"$max"'", "'"$hottestCore"'", "'"$AvgCoreCpu"'" }' >> nonpilot_cpu.report
              rm cpu_$sta.txt Cpu*
        fi
done

echo -e "Station\tCore\tAvgCPU\tMinCPU\tMaxCPU" > per_core_cpu.report
for file in `ls Sta_*_cpu.rpt`
do 
   cat $file >> per_core_cpu.report
   rm $file
done


awk 'BEGIN { printf "%16s\t%16s\n", "Nonpilot_MAX_CPU", "Nonpilot_AVG_CPU" } { if (max=="") max=$2; if ($2>=max) max=$2; sum+=$4; count++; } END { printf "%15.1f\t%15.1f\n", max, sum/count } ' nonpilot_cpu.report > nonpilot_cpu.summary

sed -n '1p' oam_cpu.report > nonpilot_cpu.tmp
cat nonpilot_cpu.report >> nonpilot_cpu.tmp
mv nonpilot_cpu.tmp nonpilot_cpu.report

paste oam_cpu.summary nonpilot_cpu.summary > top_cpu.summary
cat oam_cpu.report oam_cpu.summary nonpilot_cpu.report nonpilot_cpu.summary > top_cpu.report 
