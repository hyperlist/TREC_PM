#!/usr/bin/env bash

BASE_PATH=$(pwd)
source /etc/profile
source activate python3
#curl -X GET "localhost:9200/_nodes/stats"


rm qresults/* -rf
rm trec/* -rf
echo "query_elastic"
python query_elastic.py

path='./qresults'

mkdir trec
files=$(ls $path)
for filename in $files
do
    echo $path/$filename
   ./trec_eval-9.0/trec_eval ./data/ClinicalTrials/qrels-treceval-trials.38.txt $path/$filename >> trec/$filename'.m'
   cat trec/$filename'.m'
done

#
#wget ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/*.gz -P ./data/ScientificAbstracts/PubMed 