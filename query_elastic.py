import elasticsearch
from data import DataManager

def es_query(extracted_data):
    """
    This function is used to query Elasticsearch and write results to an output file.
    It receives a dictionary containing the extracted query terms from the extract_query_xml function. After querying Elasticsearch, the retrieved results are written to an output file in the standard trec_eval format.
    """

    try:
        # Store the disease name from the received dictionary in the variable named query
        disease_query = extracted_data['disease']
        gene_query = extracted_data['gene']
        age_query = int(extracted_data['age'])
        sex_query = extracted_data['sex']
        if extracted_data['other'] != 'None':
            aux_query = extracted_data['other']
        else:
            aux_query = None

        res = es.search(index='ct', body={
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": disease_query,
                            "fields": ["brief_title * 3", "brief_summary", "detailed_description", "eligibility",
                                       "keyword * 3",
                                       "mesh_term * 3"],
                            "boost" : 3
                        }
                    },
                    "must": {
                        "multi_match": {
                            "query": gene_query,
                            "fields": ["brief_title", "brief_summary", "detailed_description", "eligibility", "keyword",
                                       "mesh_term"],
                            "boost" : 3
                        }
                    },
                    
                    "should":{
                        "multi_match": {
                            "query" : disease_query,
                            "fields" : ["brief_summary", "detailed_description"],
                            "boost" : 1
                        }
                    },
                    
                    "filter": {
                        "range": {"maximum_age": {"gte": age_query}},
                        "range": {"minimum_age": {"lte": age_query}}
                    }
                }
            },
            "post_filter":
                {"term": {"gender": "all"},
                 },
        }, size=1000)
        
        print(res)
        
    except Exception as e:
        print("\nUnable to query/write!")
        print('Error Message:', e, '\n')
    return
if __name__ == '__main__':
    try:
        es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
    except Exception as e:
        print('Error Message:', e, '\n')
        raise Exception("\nCannot connect to Elasticsearch!")
    # Call the function to start extracting the queries
    
    topics = DataManager.extract_query_xml()
    for item in topics:
        es_query(item)

    