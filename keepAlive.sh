#!/bin/bash

dur=150
sleep_time=$dur
alive=/tmp/blockalltwerps

rm $alive

sleep $sleep_time

while true
    do

        if [ ! -f $alive ]; then
            echo "File not found! - BlockAllTwerps.py has not checked in and must be hung"
            kill -9 $1
            #exit 0
        else

            rm $alive
        fi

        sleep $sleep_time
        sleep_time=$(( $dur * 2 ))
        # the first trip through the loop is fast to catch start-up errors

done
