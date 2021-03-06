#!/bin/bash

# get the dir of this script
pushd `dirname $0` > /dev/null
program_dir=`pwd`
popd > /dev/null

#stop the service
/etc/init.d/BlockAllTwerps stop

sleep 20
cd $program_dir

while true
    do

        touch /tmp/blockalltwerps

        sleep 5

        git pull
        sleep 5

        echo "starting script"
        /usr/bin/python BlockAllTwerps.py -fullscreen &
        pid=$!

        ./keepAlive.sh $pid &
        alive_pid=$!

        wait $pid
        kill $alive_pid

        sudo shutdown -r now
        sleep 5
done
