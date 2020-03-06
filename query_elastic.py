import elasticsearch
from data import DataManager

field = ["brief_title * 2", "official_title","brief_summary", "detailed_description", "conditions", "criteria","keyword * 3","mesh_term"]

def ct_query(extracted_data):
    disease = extracted_data['disease']
    gene = extracted_data['gene']
    age = int(extracted_data['age'])
    gender = extracted_data['gender']
    other = extracted_data['other']
    if extracted_data['other'] != 'None':
        aux = extracted_data['other']
    else:
        aux = None

    res = es.search(index='ct', body={
        "query": {
            "bool": {
                "must": [
                    {"multi_match":{"query":gene,"fields":field,"boost":2}},
                    {"multi_match":{"query":disease,"fields":field,"boost":2}},
                    {"match":{"gender":gender}},
                    {"range":{"minimum_age":{"lte":age}}},
                    {"range":{"maximum_age":{"gte":age}}},
                ],
                "should": [
                    {
                      "bool": {
                        "should": {
                          "multi_match": {
                            "query": "cancer carcinoma tumor",
                            "fields": fields,
                            "tie_breaker": 0.3,
                            "type": "best_fields"
                          }
                        }
                      }
                    },
                    {
                      "bool": {
                        "should": {
                          "multi_match": {
                            "query": "gene genotype DNA base",
                            "fields": fields,
                            "tie_breaker": 0.3,
                            "type": "best_fields"
                          }
                        }
                      }
                    },
                    {
                      "bool": {
                        "should": {
                          "multi_match": {
                            "query": "surgery therapy treatment prognosis prognostic survival patient resistance recurrence targets malignancy study therapeutical outcome",
                            "fields": fields,
                            "tie_breaker": 0.3,
                            "type": "best_fields"
                          }
                        }
                      }
                    },
                    {
                      "match": {
                        "criteria": {
                          "query": other,
                          "boost": -2
                        }
                      }
                    }

                ]
            }
        },
    }, size=1500)
    
    print(res['hits']["total"],res['hits']["max_score"])
    return res['hits']['hits']
    
def show_result(res):
    print('nct_id:{}\t relevance score:{}\n'
              .format(i['_source']['nct_id'], round(res[0]['_score'] / max_score, 4)))
    print(res[0]['_source']['brief_title'])
        
def save_ct_result():
    topics = DataManager.extract_query_xml()
    rank_ctr = 1
    for item in topics:
        res = ct_query(item)
        print("query item : ",item['tnum'])
        with open('qresults/ct_results.txt', 'a') as op_file:
            for i in res:
                op_file.write(
                    '{}\tQ0\t{}\t{}\t{}\myrun\n'.format(
                        item['tnum'], i['_source']['nct_id'], rank_ctr, round(i['_score'] / max_score, 4)))
                rank_ctr += 1
        print(item['tnum']," : finish_writing")
    
if __name__ == '__main__':
    try:
        es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
    except Exception as e:
        print('Error Message:', e, '\n')
        raise Exception("\nCannot connect to Elasticsearch!")
    # Call the function to start extracting the queries
    save_ct_result()
    '''
    topics = DataManager.extract_query_xml()
    while 1:
        str = input("Enter the topic number you want to search 1~30, Enter 'q' to quit: ")
        if str == "q":
            break
        idx = int(str) - 1
        res = ct_query(topics[idx])
        show_result(res)
    '''
    