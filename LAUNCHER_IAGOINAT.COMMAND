#!/bin/sh
echo Starting InaturalistSearch
export PYTHONPATH=$(dirname $0)/libs:$(dirname $0)/src/
cd $(dirname $0)/src
python -W ignore ./InaturalistSearch.py
echo Done