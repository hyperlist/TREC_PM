import elasticsearch
import json,re,time,sys
import DataManager
import os 

re_folder = './qresults'

def construct_ct_query(template, extracted_data):
    disease = extracted_data['disease']
    gene = extracted_data['gene']
    gene1 = extracted_data['gene1']
    age = extracted_data['age']
    sex = extracted_data['gender']
    other = extracted_data['other']
    diseasePreferredTerm = extracted_data['diseasePreferredTerm']
    diseaseSynonyms = extracted_data['diseaseSynonyms']
    diseaseHypernyms = extracted_data['diseaseHypernyms']
    geneSynonyms = extracted_data['geneSynonyms']
    geneDescriptions = extracted_data['geneDescriptions']
    #print(template)
    seq = " "
    template = template.replace('{{age}}', str(age))
    template = template.replace('{{gene}}', gene)
    template = template.replace('{{gene1}}', gene1)
    template = template.replace('{{disease}}',disease)
    template = template.replace('{{sex}}',sex)
    template = template.replace('{{other}}',str(other))
    template = template.replace('{{diseasePreferredTerm}}', str(diseasePreferredTerm))
    template = template.replace('{{[geneDescriptions]}}',str(geneDescriptions))
    template = template.replace('{{[diseaseSynonyms]}}',seq.join(diseaseSynonyms))
    template = template.replace('{{[diseaseHypernyms]}}',seq.join(diseaseHypernyms))
    template = template.replace('{{[geneSynonyms]}}',seq.join(geneSynonyms))
    #print(re.findall(r'{{(.*)}}',temp))
    #l = temp.split('\n')
    #for i in range(len(l)):
    #    print(i," ", l[i])
    return json.loads(template)
    
#curl -XGET 'http://localhost:9200/ct/xml/_validate/query?explain' -H 'Content-Type: application/json' -d @test.txt
        
def get_ct_result():
    path = 'template/clinical_trials/'
    file_list = list(os.listdir(path))
    topics = DataManager.extract_query_extension()
    
    
    if (not os.path.exists(re_folder)):
        os.makedirs(re_folder)
    for file in file_list:
        name = file.split('.')[0]
        print(name,' start ')
        temp = DataManager.get_template(os.path.join('clinical_trials', file))
        
        op_file = open(os.path.join(re_folder, name+'.txt'), 'w')
        for item in topics:
            query = construct_ct_query(temp, item)
            rank_ctr = 1
            print('query topic: ',item['tnum'], ' disease: ', item['disease'])
            starttime = time.time()
            r = es.search(index='ct', body=query, size=1000,request_timeout=120)
            res = r['hits']['hits']
            for i in res:
                op_file.write('{}\tQ0\t{}\t{}\t{}\t{}\n'.format(item['tnum'], i['_source']['id'], rank_ctr, round(i['_score'], 4), name))
                rank_ctr += 1
            print('query topic: ', item['tnum'], " spend time :", time.time() - starttime)
        print(name," finish")
        op_file.close()

    
def intersection_query():
    topics = DataManager.extract_query_extension()
    while 1:
        temp = input("Enter the topic number you want to search 1~30, Enter 'q' to quit: ")
        if temp == "q":
            break
        idx = int(temp) - 1
        res = ct_query(topics[idx])
        print(res[0]['_source']['id'], res[0]['_score'])
        print(res[1]['_source']['id'], res[1]['_score'])
        print(res[2]['_source']['id'], res[2]['_score'])
    
if __name__ == '__main__':
    
    
    try:
        es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
    except Exception as e:
        print('Error Message:', e, '\n')
        raise Exception("\nCannot connect to Elasticsearch!")
    # Call the function to start extracting the queries
    get_ct_result()
    #intersection_query()
    