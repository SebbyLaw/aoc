#!/usr/bin/bash

# input should be <year> <day>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <year> <day>"
    exit 1
fi

if [ $2 -lt 1 ] || [ $2 -gt 25 ]; then
    echo "Day must be between 1 and 25"
    exit 1
fi

CURRENT_YEAR=$(date +%Y)

if [ $1 -lt 2015 ] || [ $1 -gt $CURRENT_YEAR ]; then
    echo "Year must be between 2015 and $CURRENT_YEAR (current year)"
    exit 1
fi

set -e

COPYING_TO=sols/$1/$(printf "%02d" $2).py

echo "Creating $COPYING_TO"
mkdir -p sols/$1

cp -i template.py $COPYING_TO
code $COPYING_TO
