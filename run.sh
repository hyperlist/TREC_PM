#!/usr/bin/env bash

BASE_PATH=$(pwd)

source activate python3
pip install nltk urllib3
pip install elasticsearch

echo "Calculating Precision"
cd trec_eval.9.0
make clean
make
./trec_eval ../data/ClinicalTrials/qrels-final-trials.txt ../qresults/results.txt
