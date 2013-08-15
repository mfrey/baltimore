#!/bin/zsh

if [ "$#" -lt 2 ] || ! [ -d "$2" ]; then
    echo "Usage: $0 SCENARIONAME DIRECTORY [OPTIONAL_BALTIMORE_PARAMS]" >&2
    exit 1
fi

local scenario=$1
local folder=$2
local optionalParams=$3

echo "Analysing $scenario in $folder"

for i in 0 150 300 450 600 750 900; do
    echo "Analysing $scenario$i"
    ./main.py -d $folder -s $scenario$i -e $optionalParams >&! report/$scenario$i.analysis.txt
done

echo "FINISHED"

