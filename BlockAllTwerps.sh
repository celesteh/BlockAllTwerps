#!/bin/bash

# get the dir of this script
pushd `dirname $0` > /dev/null
program_dir=`pwd`
popd > /dev/null

sleep 20

while true
    do
      cd $program_dir
      /usr/bin/python BlockAllTwerps.py -fullscreen
      sleep 5
done
