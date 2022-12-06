#!/bin/sh

#update files from github

for file in /home/mendel/ekmeksay/*
do
    if [ -d "$file" ]
    then
        echo "$file is a directory"
    elif [ -f "$file" ]
    then
        echo "$file is a file"
        sudo rm -r $file
    fi
done
