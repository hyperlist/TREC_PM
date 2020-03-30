#!/usr/bin/env bash

#BASE_PATH=$(pwd)
#source /etc/profile
#source activate python3
#curl -X GET "localhost:9200/_nodes/stats"

#rm trec/* -rf
#rm template -rf

rm qresults/* -rf
echo "query_elastic"
python query_elastic.py

path='./qresults'

rm trec.m -rf

files=$(ls $path)
for filename in $files
do
    echo $path/$filename
   ./trec_eval-9.0/trec_eval ./data/ClinicalTrials/qrels-treceval-trials.38.txt $path/$filename >> trec.m 
done
cat trec.m 

#wget ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed20n0004.xml.gz -P ./data/ScientificAbstracts/PubMed 