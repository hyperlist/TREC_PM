import http.client
import json,time
from urllib.parse import quote
from data import DataManager
from xml.etree.ElementTree import Element

conn = http.client.HTTPSConnection("api.lexigram.io")

payload = "{}"

headers = {
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdSI6Imx4ZzphcGkiLCJzYyI6WyJrZzpyZWFkIiwiZXh0cmFjdGlvbjpyZWFkIl0sImFpIjoiYXBpOjI2ZmJiY2E1LTQ5NjMtMzg5MC1hZWUzLWIxZTBhY2MzZGQxNiIsInVpIjoidXNlcjo0Yjc3YTYxYS04ODIwLTllMzgtNzk4ZC03OTQ4YWRmOTE3YjciLCJpYXQiOjE1ODMxNDM4OTd9.yCmuudsjWTAcfcixOoEb_IfIsplvRWYDRffUMHJpRng",
    'content-type': "application/json"
    }
    
def QueryExpansion(name):
    query = {}
    try:
        conn.request("GET", "/v1/lexigraph/search/?limit=10&q="+quote(name), payload, headers)
        res = str(conn.getresponse().read(),'utf-8')
        res = json.loads(res)
        conceptSearchHits = res[ 'conceptSearchHits']
        if res['totalHitsCount'] > 0:
            concept = conceptSearchHits[0]['concept']
            query['preferredTerm'] = concept['label']
            query['Synonyms'] = GetSynonyms(concept['id'])
    except:
        print(name)
        print(res)
    time.sleep(2)
    return query
    
def GetSynonyms(concept_id):
    conn.request("GET", "/v1/lexigraph/concepts/" + concept_id + "/ancestors?page=1", payload, headers)
    res = str(conn.getresponse().read(),'utf-8')
    res = json.loads(res)
    Synonyms = []
    for item in res[ 'results']:
        Synonyms.append(item['label'])
    return Synonyms

if __name__ == '__main__':
    topics = DataManager.extract_query_xml()
   
    savejson = open('data/2019_extension' +'.json','a',encoding='utf-8')
    for item in topics:
        print(item)
        item['disease_extension'] = QueryExpansion(item['disease'])
        item['gene_extension'] = QueryExpansion(item['gene'])
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        savejson.write(line)
    savejson.close()
    
    