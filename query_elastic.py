import elasticsearch
import json,re,time
import sys
from data import DataManager

def ct_query(extracted_data):
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
    temp = DataManager.matchval('ct_boost.json')
    
    temp = temp.replace('"{{age}}"',str(age))
    temp = temp.replace('{{gene}}',gene)
    temp = temp.replace('{{disease}}',disease)
    temp = temp.replace('{{sex}}',sex)
    temp = temp.replace('{{other}}',str(other))
    seq = ' '
    temp = temp.replace('{{diseasePreferredTerm}}', str(diseasePreferredTerm))
    temp = temp.replace('"{{[diseaseSynonyms]}}"','"'+seq.join(diseaseSynonyms)+'"')
    temp = temp.replace('"{{[diseaseHypernyms]}}"','["'+seq.join(diseaseHypernyms)+'"]')
    #temp = temp.replace('{{[customDiseaseExpansions]}}',str(diseaseSynonyms))     #customDiseaseExpansions
    temp = temp.replace('"{{[geneSynonyms]}}"','["'+seq.join(geneSynonyms)+'"]')
    #temp = temp.replace('{{[geneHypernyms]}}',str(geneSynonyms))
    #temp = temp.replace('{{[customGeneExpansions]}}',str(geneSynonyms))
    temp = temp.replace('"{{[geneDescriptions]}}"','["'+seq.join(geneDescriptions)+'"]')
    
    query = json.loads(temp)
    print(query)
    r = es.search(index='ct', body=query, size=500,request_timeout=120)
    #print(res['hits']["total"],res['hits']["max_score"])
    return r
        
def save_ct_result():
    topics = DataManager.extract_query_extension()
    f = open('qresults/ct_results.txt', 'w')
    f.close()
    for item in topics:
        rank_ctr = 1
        print('query topic: ',item['tnum'], ' disease: ', item['disease'])
        starttime = time.time()
        r = ct_query(item)
        max_score = r['hits']["max_score"]
        num = r['hits']["total"]
        res = r['hits']['hits']
        with open('qresults/ct_results.txt', 'a') as op_file:
            for i in res:
                op_file.write('{}\tQ0\t{}\t{}\t{}\tmyrun\n'.format(item['tnum'], i['_source']['nct_id'], rank_ctr, round(i['_score'] / max_score, 4)))
                rank_ctr += 1
        print(item['tnum']," spend time :", time.time() - starttime)
        
        print('total is : ', num, 'ac number is ', len(res))
        
def show_result(r):
    max_score = r['hits']["max_score"]
    res = r['hits']['hits']
    print('nct_id:{}\t relevance score:{}\n'
              .format(i['_source']['nct_id'], round(res[0]['_score'] / max_score, 4)))
    print(res[0]['_source']['brief_title'])
    
def intersection_query():
    topics = DataManager.extract_query_extension()
    while 1:
        temp = input("Enter the topic number you want to search 1~30, Enter 'q' to quit: ")
        if temp == "q":
            break
        idx = int(temp) - 1
        r = ct_query(topics[idx])
        show_result(r)
    
if __name__ == '__main__':
    try:
        es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
    except Exception as e:
        print('Error Message:', e, '\n')
        raise Exception("\nCannot connect to Elasticsearch!")
    # Call the function to start extracting the queries
    save_ct_result()
    #intersection_query()
    