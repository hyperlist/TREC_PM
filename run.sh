#!/usr/bin/env bash

source activate python3

BASE_PATH=$(pwd)

pip install nltk urllib3
pip install elasticsearch

echo "Creating index, it takes a long time..."
python extract_ct_data.py

echo "Training..."
python query_train.py

echo "Testing..."
python query_test.py

echo "Calculating Precision"
cd trec_eval.9.0
make clean
make
./trec_eval $BASE_PATH/data/ClinicalTrials/qrels-final-trials.txt $BASE_PATH/results/results.txt
