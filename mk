#!/usr/bin/bash

# input should be <year> <day>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <year> <day>"
    exit 1
fi

set -e

COPYING_TO=src/$1/$2.py

echo "Creating $COPYING_TO"
mkdir -p src/$1

cp -i template.py $COPYING_TO
code $COPYING_TO
