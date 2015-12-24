#!/usr/bin/env bash

# install virtualenv
check=`virtualenv --version`
[ $? != 0 ] && sudo pip2.7 install virtualenv

# check for virtualenv
python2.7 -m virtualenv env

# activate virtualenv
source env/bin/activate

# install
pip2.7 install --upgrade pip
pip2.7 install -r requirements.txt

echo "[OK] Installation complete."
