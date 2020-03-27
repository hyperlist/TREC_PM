import elasticsearch
import os
import DataManager
import numpy as np
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  

rfile = './data/ClinicalTrials/qrels-treceval-trials.38.txt'
topics = DataManager.extract_query_extension()
num = 50
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
            if (id < int(temp[0]) or i==len(lines)-2): 
                tfidffile = open(sFilePath+'tfidf'+str(id),'w')
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
                '''
                testfile = open(sFilePath+'test.'+str(id),'w')
                '''
                corpus = []
                id = int(temp[0])
                cnt = num
                


'''           
file = './data/ScientificAbstracts/qrels-treceval-abstracts.2019.txt'
with open(file,'r') as f:
    cnt = 20
    id = 1
    lines = f.readlines()
    for i in range(len(lines)-1):
        temp = lines[i+1].split(' ')
        if(cnt==20):
            sFilePath = 'test-sa'
            if not os.path.exists(sFilePath) : 
                os.mkdir(sFilePath)
            file = open(sFilePath+'/test.,'w')
            for k,v in topics[id-1].items():
                file.write(k+':'+str(v))
                file.write(' ')
        if cnt > 0:
            id = lines[i].split(' ')[2]
            print(items)
            dsl = {
                'query': {
                    'ids' : id
                }
            }
            result = es.search(index='sa', doc_type='doc', body=dsl)
            data = result['hits']['hits']
            for k,v in data.items():
                file.write(k+':'+str(v))
                file.write('\n')
            file.write('\n')
            cnt -= 1
        else:
            if id < int(temp[0]):
                id = int(temp[0])
                cnt = 20
'''