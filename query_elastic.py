import elasticsearch
import json,re,time,sys
from data import DataManager
    
template = 'BASE.json'

def construct_ct_query(extracted_data):
    disease = extracted_data['disease']
    gene = extracted_data['gene']
    age = extracted_data['age']
    sex = extracted_data['gender']
    other = extracted_data['other']
    diseasePreferredTerm = extracted_data['diseasePreferredTerm']
    diseaseSynonyms = extracted_data['diseaseSynonyms']
    diseaseHypernyms = extracted_data['diseaseHypernyms']
    geneSynonyms = extracted_data['geneSynonyms']
    geneDescriptions = extracted_data['geneDescriptions']
    
    #获取查询模板
    temp = DataManager.get_template(template)
    
    seq = " "
    temp = temp.replace('{{age}}',str(age))
    temp = temp.replace('{{gene}}',gene)
    temp = temp.replace('{{disease}}',disease)
    temp = temp.replace('{{sex}}',sex)
    temp = temp.replace('{{other}}',str(other))
    temp = temp.replace('{{diseasePreferredTerm}}', str(diseasePreferredTerm))
    temp = temp.replace('{{[geneDescriptions]}}',str(geneDescriptions))
    temp = temp.replace('{{[diseaseSynonyms]}}',seq.join(diseaseSynonyms))
    temp = temp.replace('{{[diseaseHypernyms]}}',seq.join(diseaseHypernyms))
    #temp = temp.replace('{{[customDiseaseExpansions]}}',str(diseaseSynonyms))     #customDiseaseExpansions
    temp = temp.replace('{{[geneSynonyms]}}',seq.join(geneSynonyms))
    #temp = temp.replace('{{[geneHypernyms]}}',str(geneSynonyms))
    #temp = temp.replace('{{[customGeneExpansions]}}',str(geneSynonyms))
    #print(re.findall(r'{{(.*)}}',temp))
    #l = temp.split('\n')
    #for i in range(len(l)):
    #    print(i," ", l[i])
    return json.loads(temp)
    
#curl -XGET 'http://localhost:9200/ct/xml/_validate/query?explain' -H 'Content-Type: application/json' -d @test.txt
def ct_query(extracted_data):
    query = construct_ct_query(extracted_data)
    #print(query)
    r = es.search(index='ct', body=query, size=500,request_timeout=120)
    print('total is : ', r['hits']["total"], 'ac number is ', len(r['hits']['hits']))
    return r['hits']['hits']
        
def save_ct_result():
    topics = DataManager.extract_query_extension()
    op_file = open('qresults/ct_results.txt', 'w')
    for item in topics:
        rank_ctr = 1
        print('query topic: ',item['tnum'], ' disease: ', item['disease'])
        starttime = time.time()
        res = ct_query(item)
        for i in res:
            op_file.write('{}\tQ0\t{}\t{}\t{}\tbaseline\n'.format(item['tnum'], i['_source']['nct_id'], rank_ctr, round(i['_score'], 4)))
            rank_ctr += 1
        print(item['tnum']," spend time :", time.time() - starttime)
    op_file.close()
    
    
def intersection_query():
    topics = DataManager.extract_query_extension()
    while 1:
        temp = input("Enter the topic number you want to search 1~30, Enter 'q' to quit: ")
        if temp == "q":
            break
        idx = int(temp) - 1
        res = ct_query(topics[idx])
        print(res[0]['_source']['nct_id'], res[0]['_score'])
        print(res[1]['_source']['nct_id'], res[1]['_score'])
        print(res[2]['_source']['nct_id'], res[2]['_score'])
    
if __name__ == '__main__':
    
    
    try:
        es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
    except Exception as e:
        print('Error Message:', e, '\n')
        raise Exception("\nCannot connect to Elasticsearch!")
    # Call the function to start extracting the queries
    save_ct_result()
    intersection_query()
    