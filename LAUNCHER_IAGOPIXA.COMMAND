#!/bin/sh
echo Starting PixabaySearch
export PYTHONPATH=$(dirname $0)/libs:$(dirname $0)/src/
cd $(dirname $0)/src
python -W ignore ./PixabaySearch.py
echo Done