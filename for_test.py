import elasticsearch
import DataManager

file = './data/ClinicalTrials/qrels-treceval-trials.38.txt'
topics = DataManager.extract_query_xml()
with open(file,'r') as f:
    cnt = 20
    id = 1
    lines = f.readlines()
    for i in range(len(lines)-1):
        temp = lines[i+1].split(' ')
        if(cnt==20):
            file = open('test-ct/test.'+str(id),'w')
            for k,v in topics[id-1].items():
                file.write(k+':'+str(v))
                file.write(' ')
        if cnt > 0:
            print(lines[i])
            id = lines[i].split(' ')[2]
            data = DataManager.ct_extract(doc_id=id)
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
file = './data/ScientificAbstracts/qrels-treceval-abstracts.2019.txt'
with open(file,'r') as f:
    cnt = 20
    id = 1
    lines = f.readlines()
    for i in range(len(lines)-1):
        temp = lines[i+1].split(' ')
        if(cnt==20):
            file = open('test-sa/test.'+str(id),'w')
            for k,v in topics[id-1].items():
                file.write(k+':'+str(v))
                file.write(' ')
        if cnt > 0:
            id = lines[i].split(' ')[2]
            print(items)
            dsl = {
                'query': {
                    'match': {
                        'id': id
                    }
                }
            }
            result = es.search(index='news', doc_type='politics', body=dsl)
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