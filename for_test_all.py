import elasticsearch
import os
import DataManager
import numpy as np
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  

rfile = './data/ClinicalTrials/qrels-treceval-trials.38.txt'
topics = DataManager.extract_query_extension()
num = 100
sFilePath = 'test-ct/'
if not os.path.exists(sFilePath) : 
    os.mkdir(sFilePath)
    
vectorizer=CountVectorizer(stop_words='english')
transformer=TfidfTransformer() 

with open(rfile,'r') as f:
    cnt = num
    id = 1
    corpus=[]
    lines = f.readlines()
    #testfile = open(sFilePath+'test.'+str(id),'w')
    
    for i in range(len(lines)-1):
        temp = lines[i+1].split(' ')
        if cnt > 0:
            tid = lines[i].split(' ')[2]
            data = DataManager.ct_extract(doc_id=tid)
            line = data['title'] + str(data['summary']) + str(data['detailed_description']) + str(data['inclusion'])
            corpus.append(line)
            '''
            for k,v in data.items():
                testfile.write('['+ str(num-cnt+1) +']')
                testfile.write(k+':'+str(v))
                testfile.write('\n')
            testfile.write('\n')
            '''
            cnt -= 1
        else:
            if (id < int(temp[0])): 
                '''
                testfile = open(sFilePath+'test.'+str(id),'w')
                corpus = []
                '''
                id = int(temp[0])
                cnt = num
                
tfidffile = open('tfidf','w')
X = vectorizer.fit_transform(corpus)
word=vectorizer.get_feature_names()
print(len(word)) 
Y=transformer.fit_transform(X) 
weight=np.array(Y.toarray())
mean = np.mean(weight,axis=0)
tfidf = {}
for j in range(len(word)):  
    tfidf[word[j]] = round(mean[j],3)

tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
for k in tfidf:
    tfidffile.write(k[0] + ' ' + str(k[1]))
    tfidffile.write('\n')
