import glob
import xml.etree.ElementTree as ET
import collections
import elasticsearch
import time
from multiprocessing import Pool
import DataManager

ctr_list = [0, 100000, 200000, 300000, 400000]
sa_list = [0, 253, 506, 759, 1016]

data_root='./data'

def extract_ct_xml(kernel_index):
    print('\nProgress:',kernel_index)
    list_of_files = []
    file_path = data_root + "/ClinicalTrials/clinical_trials." + str(kernel_index) + "/*/*"
    list_of_files += glob.glob(file_path)
    print(len(list_of_files))
    ctr = ctr_list[kernel_index]
    start_time = time.time()
    for input_file in list_of_files:
        extracted_data = DataManager.ct_extract(path=input_file)
        es_index('ct', ctr, extracted_data)
        ctr = ctr + 1
        if(ctr%300==0):
            print('kernel_index', kernel_index,' at ',ctr)
            print("\nExecution time: %.2f seconds" % (time.time() - start_time))
    print(kernel_index,' finish ',file_path)

def es_index(index, id, extracted_data):
    #curl -H 'Content-Type:application/json' -XGET http://localhost:9200/ct/xml/1?pretty
    #curl -X GET "localhost:9200/ct/xml/1?pretty"
    try:
        es.index(index=index, doc_type='doc', id=id, body=extracted_data)
    except Exception as e:
        print('Document not indexed!')
        print('Error Message:', e)
    return


def extract_sa_xml(kernel_index):
    print('\nProgress:',kernel_index)
    # Provide the path to the input xml files
    list_of_files = []
    start_time = time.time()
    cnt = 0;
    for i in range(sa_list[kernel_index],sa_list[kernel_index+1]):
        file_path = data_root + "/ScientificAbstracts/PubMed/pubmed20n"+str(i).rjust(5,'0') +".xml.gz"
        #print(file_path)
        data = DataManager.ct_extract(path=input_file)
        for extracted_data in data:
            es_index('sa', extracted_data['id'], extracted_data)
        if(cnt%300==0):
            print('kernel_index', kernel_index,' at ',cnt)
            print("\nExecution time: %.2f seconds" % (time.time() - start_time))
    print(kernel_index,' finish ')


if __name__ == '__main__':
    try:
        es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
    except Exception as e:
        print('\nCannot connect to Elasticsearch!')
        print('Error Message:', e, '\n')
        raise Exception("\nCannot connect to Elasticsearch!")
    
    start_time = time.time()
    # create process pool
    p = Pool(4)
    for i in range(4):
        p.apply_async(extract_ct_xml, args=(i,))
    p.close()
    p.join()
    print("\nExecution time: %.2f seconds" % (time.time() - start_time))
   