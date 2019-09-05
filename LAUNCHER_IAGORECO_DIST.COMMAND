#!/bin/sh
echo Starting Reco
export PYTHONPATH=$(dirname $0)/libs:$(dirname $0)/src/
cd $(dirname $0)/src
python -W ignore ./asr.py 45001 192.168.3.10 45000 8080
