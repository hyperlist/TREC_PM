import glob
import xml.etree.ElementTree as ET
import collections
import elasticsearch
import time
from multiprocessing import Pool
from data import DataManager

# Divide xml data into 8 groups and process them with 8 processes
ctr_list = [0, 100000,  200000, 300000, 400000]

data_root='./data'

def extract_ct_xml(kernel_index):
    print('\nProgress:',kernel_index)
    # Provide the path to the input xml files
    list_of_files = []
    file_path = data_root + "/ClinicalTrials/clinical_trials." + str(kernel_index) + "/*/*"
    list_of_files += glob.glob(file_path)
    print(len(list_of_files))
    ctr = ctr_list[kernel_index]
    for input_file in list_of_files:
        extracted_data = DataManager.ct_extract(path=input_file)
        ct_index(ctr, extracted_data)
        ctr = ctr + 1
        if(ctr%300==0):
            print('kernel_index', kernel_index,' at ',ctr)
    print(kernel_index,' finish ',file_path)

def ct_index(ctr, extracted_data):
    #curl -H 'Content-Type:application/json' -XGET http://localhost:9200/ct/xml/1?pretty
    #curl -X GET "localhost:9200/ct/xml/1?pretty"
    try:
        es.index(index='ct', doc_type='xml', id=ctr, body=extracted_data)
    except Exception as e:
        print('Document not indexed!')
        print('Error Message:', e)
    return



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

    # Print the total execution time
    print("\nExecution time: %.2f seconds" % (time.time() - start_time))
   