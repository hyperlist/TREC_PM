#!/usr/bin/env bash

BASE_PATH=$(pwd)

source activate python3
pip install nltk urllib3
pip install elasticsearch
echo "xml_to_elastic"
python xml_to_elastic.py
echo "query_elastic"
python query_elastic.py
echo "Calculating Precision"
cd trec_eval-9.0
make clean
make
cd ../
#2019
./trec_eval-9.0/trec_eval ./data/ClinicalTrials/qrels-treceval-trials.38.txt ./qresults/ct_results.txt
./trec_eval-9.0/trec_eval ./data/ClinicalTrials/qrels-treceval-trials.38.txt ./qresults/ct_results.txt > ./qresults/baseline_2019.log
#2017
./trec_eval-9.0/trec_eval ./data/ClinicalTrials/qrels-final-trials.txt ./qresults/results.txt > ./qresults/results.log
