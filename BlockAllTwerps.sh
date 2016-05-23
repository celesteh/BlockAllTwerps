#!/bin/bash

# get the dir of this script
pushd `dirname $0` > /dev/null
program_dir=`pwd`
popd > /dev/null

while true
    do
      cd $program_dir
      python BlockAllTwerps.py -fullscreen
      sleep 1
done
