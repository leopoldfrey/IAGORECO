#!/bin/sh
echo Starting BotResponse
export PYTHONPATH=$(dirname $0)/libs:$(dirname $0)
cd $(dirname $0)
python ./botresponse.py
echo Done