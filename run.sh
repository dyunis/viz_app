#!/usr/bin/sh

if [ $# -ne 1 ]; then
  echo "call this script as ./run.sh [path to json or directory]"
  exit 1
fi

if [ -f $1 ]; then
  cp $1 data/data.json
elif [ -d $1 ]; then
  if [ ! -d data/$1 ]; then
    mkdir data/$1
  fi
  cp $1 data/$1
else
  echo "$1 is neither a file nor a directory"
fi

python app.py
