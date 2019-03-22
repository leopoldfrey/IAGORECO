#!/bin/sh

cd $(dirname $0)

echo opening IAGOPIXA
open ./LAUNCHER_IAGOPIXA.COMMAND &

echo opening IAGOINAT
open ./LAUNCHER_IAGOINAT.COMMAND &

echo opening IAGOGOGOL
open ./LAUNCHER_IAGOGOGOL.COMMAND &

echo opening IAGORECO
open ./LAUNCHER_IAGORECO.COMMAND &

echo opening IAGOGOTCHI
open ./Reco+Pixa+Inat+Gogol.maxpat &

echo opening ASR webpage
open -a "Google Chrome" http://localhost:8080
