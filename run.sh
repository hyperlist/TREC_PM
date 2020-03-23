#!/usr/bin/env bash

BASE_PATH=$(pwd)
source /etc/profile
source activate python3
pip install nltk urllib3
pip install elasticsearch

echo "xml_to_elastic"
python xml_to_elastic.py

echo "query_elastic"
python query_elastic.py

echo "xml_to_elastic"
python for_test.py

echo "Calculating Precision"
cd trec_eval-9.0

make clean
make
cd ../
#2017
./trec_eval-9.0/trec_eval ./data/ClinicalTrials/qrels-final-trials.txt ./qresults/results.txt > ./qresults/results.log

path='./qresults'
files=$(ls $path)
for filename in $files
do
    echo $path/$filename
   ./trec_eval-9.0/trec_eval ./data/ClinicalTrials/qrels-treceval-trials.38.txt $path/$filename >> $path/$filename'.m'
done
