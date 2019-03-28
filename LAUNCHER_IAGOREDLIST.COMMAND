#!/bin/sh
echo Starting RedlistSearch
#export PYTHONPATH=$(dirname $0)/libs:$(dirname $0)/src/
cd $(dirname $0)/src
python3.7 -W ignore ./RedlistSearch.py
echo Done