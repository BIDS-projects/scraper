#!/usr/bin/env bash

# check for virtualenv
[ -d "env" ] && python2.7 -m virtualenv env

# activate virtualenv
source env/bin/activate
