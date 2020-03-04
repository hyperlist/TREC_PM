import xml.etree.ElementTree as ET
import glob 
import collections
import os,re

data_root='./data'

def extract_query_xml():
    query_file = open(os.path.join(data_root, "topics2019.xml"), "r")

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
        #print(gene)
        try:
            m = re.findall( r'(.*) [(](.*?)[)]', gene)
            extracted_data['gene'] = m[0][0]
            extracted_data['gene_code'] = m[0][1]
        except:
            extracted_data['gene'] = item.find('gene').text
            extracted_data['genecode'] = None
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
            extracted_data['sex'] = demographic.split(' ')[1]
        except:
            extracted_data['sex'] = None
        try:
            extracted_data['other'] = item.find('other').text
        except:
            extracted_data['other'] = None
        datas.append(extracted_data)
        
    #for item in datas:
    #    print(item)
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
    tree = ET.parse(file_list[0])
    root = tree.getroot()
    extracted_data = collections.OrderedDict()
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

    # overall_status
    try:
        overall_status = root.find('overall_status').text
        extracted_data['overall_status'] = overall_status
    except:
        extracted_data['overall_status'] = None

    # condition
    try:
        condition = root.find('condition').text
        extracted_data['condition'] = condition
    except:
        extracted_data['condition'] = None

    # eligibility
    try:
        eligibility = root.find('eligibility').find('criteria').find('textblock').text
        extracted_data['eligibility'] = eligibility
    except:
        extracted_data['eligibility'] = None

    # gender
    try:
        gender = root.find('eligibility').find('gender').text
        extracted_data['gender'] = gender
    except:
        extracted_data['gender'] = None

    # gender_based
    try:
        gender_based = root.find('eligibility').find('gender_based').text
        extracted_data['gender_based'] = gender_based
    except:
        extracted_data['gender_based'] = None

    # minimum_agect = 0
    try:
        minimum_age = root.find('eligibility').find('minimum_age').text
        try:
            extracted_data['minimum_age'] = int(minimum_age.split(' ')[0])
        except:
            extracted_data['minimum_age'] = 0
    except:
        extracted_data['minimum_age'] = None

    # maximum_age
    try:
        maximum_age = root.find('eligibility').find('maximum_age').text
        try:
            extracted_data['maximum_age'] = int(maximum_age.split(' ')[0])
        except:
            extracted_data['maximum_age'] = 99
    except:
        extracted_data['maximum_age'] = None

    # keyword
    try:
        keyword = root.findall('keyword')
        for index, item in enumerate(keyword):
            keyword_list.append(item.text)
        extracted_data['keyword'] = keyword_list
    except:
        extracted_data['keyword'] = None

    # mesh_term
    try:
        mesh_term = root.find('condition_browse').findall('mesh_term')
        for index, item in enumerate(mesh_term):
            mesh_term_list.append(item.text)
        extracted_data['mesh_term'] = mesh_term_list
    except:
        extracted_data['mesh_term'] = None

    # print(extracted_data)
    return extracted_data

if __name__ == '__main__':
    extract_query_xml()
