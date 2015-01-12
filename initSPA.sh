#!/bin/bash
#currentTime=`date +%T`
for ((i=1; i<=5; i++))
do
        echo "########################################"
        echo "Loop $i time starts at `date +%T`."
        echo "########################################"
        echo "Remove SPA starts at `date +%T`."
        /sn/cr/cepexec RMV_SPA rmv:spa=OAM422
        echo "Remove SPA completes at `date +%T`."
        sleep 2
        echo "Delete SPA starts at `date +%T`."
        /sn/cr/cepexec DELETE_SPA delete:spa=OAM422,proc
        echo "Delete SPA completes at `date +%T`."
        sleep 2
        echo "Install SPA starts at `date +%T`."
        /sn/cr/cepexec INSTALL_SPA install:spa=OAM422,proc
        echo "Install SPA completes at `date +%T`."
        sleep 2
        echo "Restart SPA starts at `date +%T`."
        /sn/cr/cepexec RST_SPA rst:spa=OAM422
        echo "Restart SPA completes at `date +%T`."
        echo "########################################"
        echo "Loop $i time completes at `date +%T`."
        echo "########################################"
        sleep 5
done