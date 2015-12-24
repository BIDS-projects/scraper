#!/usr/bin/env bash

echo '1 check:'

exit=`python2.7 --version`
[ $? != 0 ] && echo '[Error] Python2.7 not found' || echo '[OK] Python2.7 found'
