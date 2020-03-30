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

def es_index(index, id, extracted_data):
    #curl -H 'Content-Type:application/json' -XGET http://localhost:9200/ct/doc/1?pretty
    #curl -X GET "localhost:9200/ct/doc/_search?q=id:NCT00001685"
    try:
        es.index(index=index, doc_type='doc', id=id, body=extracted_data)
    except Exception as e:
        print('Document not indexed!')
        print('Error Message:', e)
    return

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

def extract_sa_xml(kernel_index):
    #curl -H 'Content-Type:application/json' -XGET http://localhost:9200/sa/doc/_search
    
    for i in range(227, 1016):
        #print(i,i % 4 ,kernel_index)
        if(i % 4 == kernel_index):
            start_time = time.time()
            file_path = data_root + "/ScientificAbstracts/PubMed/pubmed20n"+str(i+1).rjust(4,'0') +".xml.gz"
            #print('[kennel', kernel_index, 'start] ', file_path)
            data = DataManager.sa_extract(path=file_path)
            for extracted_data in data:
                es_index('sa', extracted_data['id'], extracted_data)
            print('[kennel', kernel_index, 'finish] ', file_path)
            print("Execution time: %.2f seconds" % (time.time() - start_time))
            '''
            '''
             
def extract_sa_xml_lost(num):
    file_path = data_root + "/ScientificAbstracts/PubMed/pubmed20n"+str(num).rjust(4,'0') +".xml.gz"
    print('[start]  ', file_path)
    data = DataManager.sa_extract(path=file_path)
    for extracted_data in data:
        es_index('sa', extracted_data['id'], extracted_data)
    print('[finish] ', file_path)
            

if __name__ == '__main__':
    try:
        es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])
    except Exception as e:
        print('\nCannot connect to Elasticsearch!')
        print('Error Message:', e, '\n')
        raise Exception("\nCannot connect to Elasticsearch!")
    
    start_time = time.time()
    
    for i in range(227, 1016):
        start_time = time.time()
        extract_sa_xml_lost(i)
        print("Execution time: %.2f seconds\n" % (time.time() - start_time))
    '''
    p = Pool(4)
    for i in range(4):
        #p.apply_async(extract_ct_xml, args=(i,))
        p.apply_async(extract_sa_xml, args=(i,))
    p.close()
    p.join()
    
    '''
   