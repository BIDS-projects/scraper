#!/usr/bin/env bash

# check for virtualenve
[ -d "env" ] && python3 -m venv env

# activate virtualenv
source env/bin/activate
