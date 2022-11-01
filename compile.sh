#!/bin/sh

## Update files from github
sudo rm -r *.pyc
git fetch
git merge origin/$CURRENT_BRANCH

## Compile all files
python3 -m compileall .
## convert all files name 
python3 renames.py 

# Remove the current files before copying  
sudo rm -r *.py

# Copy file from __pycache__ 
sudo cp -rp ./__pycache__/*.* ./

sudo rm -r __pycache__
