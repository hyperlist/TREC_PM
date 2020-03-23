import xml.etree.ElementTree as ET
import collections
import os,re
import json
import gzip
import glob

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
        file_path = glob.glob(file_path)[0]
        
    if not os.path.exists(file_path):
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
        extracted_data['id'] = nct_id
    except:
        extracted_data['id'] = None

    # brief_title
    try:
        brief_title = root.find('brief_title').text
        extracted_data['title'] = brief_title
    except:
        extracted_data['title'] = None

    # official_title
    try:
        official_title = root.find('official_title').text
        extracted_data['official_title'] = official_title
    except:
        extracted_data['official_title'] = None

    # brief_summary
    try:
        summary = root.find('brief_summary').find('textblock').text
        extracted_data['summary'] = summary.replace('\t',' ').replace('\n',' ').replace('  ','')
    except:
        extracted_data['summary'] = None

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
        criteria = root.find('eligibility').find('criteria').find('textblock').text.replace('\r\n',' ').replace('\n',' ').replace('  ',' ')
        m = re.findall('Inclusion Criteria:(.*)Exclusion Criteria:(.*)', criteria)
        extracted_data['inclusion'] = m[0][0]
        extracted_data['exclusion'] = m[0][1]
        
    except:
        extracted_data['inclusion'] = None
        extracted_data['exclusion'] = None
        
    # gender
    try:
        gender = str.lower(root.find('eligibility').find('gender').text)
        extracted_data['sex'] = gender
        if gender=="all":
            extracted_data['sex'] = "male female"
    except:
        extracted_data['sex'] = "male female"

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

def sa_extract(path=None, doc_id = None):
    if path != None:
        file_path = path
    else:
        file_path = data_root + "/ScientificAbstracts/PubMed/{}.xml.gz".format(doc_id)
    if not os.path.exists(file_path):
        print(file_path)
        raise Exception("file not exit!")
    data = []
    file = gzip.open(file_path, "r").read()
    #fstr = bytes.decode(file)
    # create xml tree
    root = ET.fromstring(file)
    #root = tree.getroot()
    print(root,len(root))
    print(root.tag,root.attrib)

    for item in root:
        #print(item)
        extracted_data = {}
        # id
        PMID = item[0][0].text
        extracted_data['id'] = PMID
        
        Article = item.find('MedlineCitation').find('Article')

        # title
        try:
            title = Article.find('ArticleTitle').text
            extracted_data['title'] = title
        except:
            extracted_data['title'] = None

        # Abstract
        try:
            abstract = Article.find('Abstract').find('AbstractText').text
            extracted_data['abstract'] = abstract
            #print(abstract)
        except:
            extracted_data['abstract'] = None
        # Date
        try:
            Date = item.find('PubmedData').find('History').find('PubMedPubDate')
            extracted_data['date'] = Date[0].text +'-'+ Date[1].text +'-'+ Date[2].text
        except:
            extracted_data['date'] = None
        data.append(extracted_data)
        #print(extracted_data)

    return data

#def read_temp(filename):
#    file_path = "./template/"
#    file = os.path.join(file_path,filename)
#    temp = open(file,mode='r',encoding='utf-8').read()
#    temp = match_subtemp(temp)
#    #print(temp)
#    return temp
    
#def match_subtemp(temp):
#    file_path = "./template/"
#    sublist = re.findall(r'{{(.*)}}',temp)
#    for item in sublist:
#        file = os.path.join(file_path,item)
#        if(os.path.exist(file)):
#            #print(item)
#            subtemp = read_temp(item)
#            #print('{{'+item+'}}')
#            temp = temp.replace('{{'+item+'}}',subtemp)
#            #temp = temp.replace('\r\n','').replace('\t','').replace('\n','').replace('  ','')
#    return temp

def get_template(filename):
    file_path = "./template/"
    file = os.path.join(file_path, filename)
    temp = open(file,mode='r',encoding='utf-8').read()
    #temp = match_subtemp(temp)
    return temp


if __name__ == '__main__':
    #query = extract_query_extension()
    #print(query['bool']['must'])
    data = sa_extract(doc_id='pubmed20n0001')
    #print(data)