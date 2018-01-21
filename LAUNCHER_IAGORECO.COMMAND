#!/bin/sh
echo Starting Reco
export PYTHONPATH=$(dirname $0)/libs:$(dirname $0)/src/
cd $(dirname $0)/src
python -W ignore ./asr.py
echo Done