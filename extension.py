import json
import pandas
import time
import requests
from urllib.parse import quote
from data import DataManager

headers = {
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdSI6Imx4ZzphcGkiLCJzYyI6WyJrZzpyZWFkIiwiZXh0cmFjdGlvbjpyZWFkIl0sImFpIjoiYXBpOjI2ZmJiY2E1LTQ5NjMtMzg5MC1hZWUzLWIxZTBhY2MzZGQxNiIsInVpIjoidXNlcjo0Yjc3YTYxYS04ODIwLTllMzgtNzk4ZC03OTQ4YWRmOTE3YjciLCJpYXQiOjE1ODMxNDM4OTd9.yCmuudsjWTAcfcixOoEb_IfIsplvRWYDRffUMHJpRng",
    'content-type': "application/json"
    }
    
def search(keyword):
    query = {}
    url = "https://api.lexigram.io/v1/lexigraph/search?q=" + keyword
    r = requests.get(url, headers=headers)
    res = json.loads(r.text)
    conceptlabel = None
    ancestors = []
    synonyms = []
    try:
        conceptid = res['conceptSearchHits'][0]['concept']['id']
        conceptlabel = res['conceptSearchHits'][0]['concept']['label']
        time.sleep(1)
        ancestors = get_ancestors(conceptid)
        time.sleep(1)
        synonyms = get_synonyms(conceptid)
    except:
        print(res)
    return conceptlabel, ancestors, synonyms
    
def get_ancestors(conceptGraphId):
    url = "https://api.lexigram.io/v1/lexigraph/concepts/" + conceptGraphId + "/ancestors"
    r = requests.get(url, headers=headers)
    response = json.loads(r.text)
    if(response['totalResults']>10):
        len = 10
    else:
        len = response['totalResults']
    ancestors = []
    for i in range(len):
        ancestors.append(response['results'][i]['label'])
    return ancestors
        
def get_synonyms(conceptGraphId):
    url = "https://api.lexigram.io/v1/lexigraph/concepts/" + conceptGraphId
    r = requests.get(url, headers=headers)
    response = json.loads(r.text)
    #print(response)
    synonyms = []
    synonyms = response['synonyms']
    return synonyms
    

if __name__ == '__main__':
    topics = DataManager.extract_query_xml()
    savejson = open('data/topics/topics2019_extension.json','w',encoding='utf-8')
    df = pandas.read_csv('data/Homo_sapiens.gene_info',delimiter = '\t')
    '''
    genecode = 'A1BG'
    row = df[(df.Symbol==genecode)]
    print()
    
    '''
    for item in topics:
        print(item)
        
        #disease
        conceptlabel, synonyms, ancestors= search(item['disease'])
        item['diseasePreferredTerm'] = conceptlabel
        item['diseaseSynonyms'] = synonyms
        item['diseaseHypernyms'] = ancestors
        #gene
        try:
            gene = item['gene1'].split(' ')[0]
            row = df[(df.Symbol==gene)]
            item['geneSynonyms'] = row.Synonyms.values[0].split('|')
            item['geneDescriptions'] = row.description.values[0]
        except: 
            gene1 = item['gene1'].split(' ')[0]
            gene = gene1.split('-')[0]
            row = df[(df.Symbol==gene)]
            item['geneSynonyms'] = row.Synonyms.values[0].split('|')
            item['geneDescriptions'] = row.description.values[0]
            gene = gene1.split('-')[1]
            row = df[(df.Symbol==gene)]
            item['geneSynonyms'] = item['geneSynonyms'] + row.Synonyms.values[0].split('|')
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        savejson.write(line)
        
    savejson.close()
    
    