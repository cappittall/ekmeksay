#!/bin/sh

## Update files from github
sudo rm -r *.pyc


## Compile all files
python3 -m compileall .
## convert all files name 
python3 renames.py 

## Copy file from __pycache__ 
sudo cp -rp ./__pycache__/*.*  ../ekmeksay
#sudo rm -r __pycache__
