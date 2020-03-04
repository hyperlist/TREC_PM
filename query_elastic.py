import elasticsearch
from data import DataManager

def ct_query(extracted_data):
    disease = extracted_data['disease']
    gene = extracted_data['gene']
    age = int(extracted_data['age'])
    sex = extracted_data['sex']
    if extracted_data['other'] != 'None':
        aux = extracted_data['other']
    else:
        aux = None

    res = es.search(index='ct', body={
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": disease,
                        "fields": ["brief_title * 3", "brief_summary", "detailed_description", "eligibility",
                                   "keyword * 3",
                                   "mesh_term * 3"],
                        "boost" : 3
                    }
                },
                "must": {
                    "multi_match": {
                        "query": gene,
                        "fields": ["brief_title", "brief_summary", "detailed_description", "eligibility", "keyword",
                                   "mesh_term"],
                        "boost" : 3
                    }
                },
                
                "should":{
                    "multi_match": {
                        "query" : disease,
                        "fields" : ["brief_summary", "detailed_description"],
                        "boost" : 1
                    }
                },
                "filter": {
                    "range": {"maximum_age": {"gte": age}},
                    "range": {"minimum_age": {"lte": age}}
                }
            }
        },
        "post_filter":
            {"term": {"gender": "all"},
             },
    }, size=1000)
    return res['hits']['hits']
    
def show_result(res):
    rank_ctr = 1
    print(res['hits']["total"],res['hits']["max_score"])
    for i in res:
        print('nct_id:{}\trelevance ranking:{}\trelevance score:{}\n'
              .format(i['_source']['nct_id'], rank_ctr, round(i['_score'] / max_score, 4)))
        rank_ctr += 1
        
def save_ct_result():
    topics = DataManager.extract_xml()
    rank_ctr = 1
    for item in topics:
        res = ct_query(item)
        with open('qresults/ct_results.txt', 'a') as op_file:
            for i in res:
                op_file.write(
                    '{}\tQ0\t{}\t{}\t{}\t2_ec_complex\n'.format(item['tnum'], i['_source']['nct_id'],
                                                                rank_ctr, round(i['_score'] / max_score, 4)))
                rank_ctr += 1

        print(item['tnum'],"finish_writing")
    
if __name__ == '__main__':
    try:
        es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
    except Exception as e:
        print('Error Message:', e, '\n')
        raise Exception("\nCannot connect to Elasticsearch!")
    # Call the function to start extracting the queries
    save_ct_result()
    topics = DataManager.extract_xml()
    while 1:
        str = input("Enter the topic number you want to search 1~30, Enter 'q' to quit: ")
        if str == "q":
            break
        idx = int(str) - 1
        res = ct_query(topics[idx])
        show_result(res)
    