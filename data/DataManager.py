import xml.etree.ElementTree as ET
import glob 
import collections
import os,re
import json

data_root='./data'

def extract_query_extension():
    lines = open(os.path.join(data_root, os.path.join("topics","topics2019_extension.json")), "r").readlines()
    datas = []
    for line in lines:
        extracted_data = json.loads(line)
        datas.append(extracted_data)
    return datas
    
def extract_query_xml():
    query_file = open(os.path.join(data_root, os.path.join("topics","topics2019.xml")), "r")

    tree = ET.parse(query_file)
    root = tree.getroot()
    datas = []
    topics = root.findall('topic')
    for index, item in enumerate(topics):
        extracted_data = {}
        extracted_data['tnum'] = index + 1
        extracted_data['disease'] = item.find('disease').text
        gene = item.find('gene').text
        demographic = item.find('demographic').text
        try:
            extracted_data['gene'] = item.find('gene').text
        except:
            extracted_data['gene'] = None
        #分解基因
        try:
            m = re.findall( r'(.*) [(](.*?)[)]', gene)
            extracted_data['gene1'] = m[0][0]
            extracted_data['gene1_code'] = m[0][1]
        except:
            extracted_data['gene1'] = item.find('gene').text
            extracted_data['gene1_code'] = None
        try:
            gene2 = gene.split(', ')[1]
        except:
            gene2 = None 
        try:
            m = re.findall( r'(.*) [(](.*?)[)]', gene2)
            extracted_data['gene2'] = m[0][0]
            extracted_data['gene2_code'] = m[0][1]
        except:
            extracted_data['gene2'] = gene2
            extracted_data['gene2_code'] = None
            
        try:
            extracted_data['age'] = int(demographic.split('-')[0])
        except:
            extracted_data['age'] = None
        try:
            extracted_data['gender'] = demographic.split(' ')[1]
        except:
            extracted_data['gender'] = None
        try:
            extracted_data['other'] = item.find('other').text
        except:
            extracted_data['other'] = None
        datas.append(extracted_data)
        
    return datas


def ct_extract(path=None, doc_id = None):
    """
    extract some fields of xml data and return extracted_data
    """
    if path != None:
        file_path = path
    else:
        file_path = data_root + "/ClinicalTrials/*/*/{}.xml".format(doc_id)
    file_list = glob.glob(file_path)
    
    if len(file_list) != 1:
        print(file_path)
        raise Exception("file not exit!")
    
    # create xml tree
    tree = ET.parse(file_path)
    root = tree.getroot()
    extracted_data = collections.OrderedDict()
    keyword_list = []
    mesh_term_list = []
    # nct_id
    try:
        nct_id = root.find('id_info').find('nct_id').text
        extracted_data['nct_id'] = nct_id
    except:
        extracted_data['nct_id'] = None

    # brief_title
    try:
        brief_title = root.find('brief_title').text
        extracted_data['brief_title'] = brief_title
    except:
        extracted_data['brief_title'] = None

    # official_title
    try:
        official_title = root.find('official_title').text
        extracted_data['official_title'] = official_title
    except:
        extracted_data['official_title'] = None

    # brief_summary
    try:
        brief_summary = root.find('brief_summary').find('textblock').text
        extracted_data['brief_summary'] = brief_summary
    except:
        extracted_data['brief_summary'] = None

    # detailed_description
    try:
        detailed_description = root.find('detailed_description').find('textblock').text
        extracted_data['detailed_description'] = detailed_description
    except:
        extracted_data['detailed_description'] = None

    # condition
    try:
        condition = root.find('condition').text
        extracted_data['condition'] = condition
    except:
        extracted_data['condition'] = None

    # criteria
    try:
        criteria = root.find('eligibility').find('criteria').find('textblock').text
        extracted_data['criteria'] = criteria.replace('\r\n',' ').replace('\n',' ').replace('  ',' ')
    except:
        extracted_data['criteria'] = None
        
    # gender
    try:
        gender = root.find('eligibility').find('gender').text
        extracted_data['gender'] = str.lower(gender)
    except:
        extracted_data['gender'] = None

    # minimum_age = 0
    try:
        minimum_age = root.find('eligibility').find('minimum_age').text
        extracted_data['minimum_age'] = int(minimum_age.split(' ')[0])
    except:
        extracted_data['minimum_age'] = 0

    # maximum_age
    try:
        maximum_age = root.find('eligibility').find('maximum_age').text
        extracted_data['maximum_age'] = int(maximum_age.split(' ')[0])
    except:
        extracted_data['maximum_age'] = 99

    # keyword
    try:
        keyword = root.findall('keyword')
        for index, item in enumerate(keyword):
            keyword_list.append(str.lower(item.text))
        extracted_data['keyword'] = keyword_list
    except:
        extracted_data['keyword'] = None

    # mesh_term
    try:
        mesh_term = root.find('condition_browse').findall('mesh_term')
        for index, item in enumerate(mesh_term):
            mesh_term_list.append(str.lower(item.text))
        extracted_data['mesh_term'] = mesh_term_list
    except:
        extracted_data['mesh_term'] = None
    # print(extracted_data)
    return extracted_data

def readtemp(filename):
    file_path = data_root + "/template/"
    file = glob.glob(file_path+filename)[0]
    temp = open(file,mode='r',encoding='utf-8').read()
    temp = matchsubtemp(temp)
    #print(temp)
    return temp
    
def matchsubtemp(temp):
    file_path = data_root + "/template/"
    sublist = re.findall(r'{{(.*)}}',temp)
    for item in sublist:
        file = glob.glob(file_path+item)
        if(len(file) == 1):
            #print(item)
            subtemp = readtemp(item)
            #print('{{'+item+'}}')
            temp = temp.replace('{{'+item+'}}',subtemp)
            #temp = temp.replace('\r\n','').replace('\t','').replace('\n','').replace('  ','')
    return temp

def matchval(name):
    str = readtemp(name)
    return str


if __name__ == '__main__':
    query = extract_query_extension()
    #print(query['bool']['must'])