#!/usr/bin/env bash

BASE_PATH=$(pwd)

source activate python3
pip install nltk urllib3
pip install elasticsearch
python xml_to_elastic.py
python query_elastic.py
echo "Calculating Precision"
cd trec_eval.9.0
make clean
make
#2019
./trec_eval ../data/ClinicalTrials/qrels-treceval-trials.38.txt ../qresults/ct_results.txt
./trec_eval ../data/ClinicalTrials/qrels-treceval-trials.38.txt ../qresults/ct_results.txt > ../res.2019
#2017
./trec_eval ../data/ClinicalTrials/qrels-final-trials.txt ../qresults/results2.txt
