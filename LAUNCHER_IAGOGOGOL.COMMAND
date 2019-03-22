#!/bin/sh
echo Starting GoogleImage
export PYTHONPATH=$(dirname $0)/libs:$(dirname $0)/src/
cd $(dirname $0)/src
python -W ignore ./GoogleImage.py
echo Done