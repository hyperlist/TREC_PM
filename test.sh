curl -XGET http://localhost:9200/ct/doc/_search   -H 'Content-Type: application/json' -d'
{
    "query":{
        "bool":{
            "must":[
                {"range":{"minimum_age":{    "lte":1    }}},
                {"range":{"maximum_age":{    "gte":98    }}},
                {"match":{    "inclusion":""}
                }
            ]
        }
    }
}'

curl -XDELETE  'localhost:9200/my_index?pretty'
curl -XGET 'localhost:9200/_cat/indices?v&pretty'

curl -XPUT 'localhost:9200/my_index?pretty' -H 'Content-Type: application/json' -d'
{
  "settings": {
    "analysis": {
        "char_filter": {
            "synonyms": {
                "type":"mapping",
                "mappings": [ "&=> and ", "colorectal => colon"]
        }},
        "filter": {
            "my_stopwords": {
                "type":"stop",
                "stopwords": [ "\n", "\t" ]
        }},
        "analyzer": {
            "my_analyzer": {
                "type:"custom",
                "char_filter":" "synonyms" ],
                "tokenizer":"standard",
                "filter":       ["my_stopwords" ]
        }}
    },
    "index" : {
        "similarity" : {
          "my_bm25" : {
            "type" : "my_bm25",
            "b" : "0.75",
            "k1" : "1"
          }
        }
    },
    "number_of_replicas": 1,
    "number_of_shards": 10
  },
  "mappings": {
    "info": {
      "properties": {
        "message": {
          "type": "text",
          "analyzer": "ik_max_word"
          , "similarity": "my_bm25"
        }
      }
    }
  }
}
'
curl -X PUT "localhost:9200/my_index?pretty" -H 'Content-Type: application/json' -d'
{
    "settings": {
        "analysis": {
        "char_filter": {
            "synonyms": {
                "type":"mapping",
                "mappings": [ "&=> and ", "colorectal => colon"]
        }},
        "filter": {
            "my_stopwords": {
                "type":"stop",
                "stopwords": [ "\n", "\t" ]
        }},
        "analyzer": {
            "my_analyzer": {
                "type:"custom",
                "char_filter":" "synonyms" ],
                "tokenizer":"standard",
                "filter":       ["my_stopwords" ]
        }}
    }
}}}
'

curl -XPUT 'localhost:9200/ct?pretty' -H 'Content-Type: application/json' -d'
{
    "settings": {
        "analysis": {
            "char_filter": {
                "synonyms": {"type":"mapping","mappings": [ "&=> and ", "colorectal => colon"]
            }},
            "filter": {
                "my_stopwords": {"type":"stop","stopwords": [ "\n", "\t" ]
            }},
            "analyzer": {
                "my_analyzer": {
                "type":"custom",
                "char_filter":" "synonyms" ],
                "tokenizer":"standard",
                "filter":["my_stopwords" ]
            }}
        },
        "similarity" : {
            "my_bm25" : {
                "type" : "BM25",
                "b" : "0.75",
                "k1" : "1"
            }
            "my_dfr" : {
                "type" : "DFR",
                "basic_model" : "g",
                "after_effect" : "l",
                "normalization" : "h2",
                "normalization.h2.c" : "2.0"
            },
            "my_ib" : {
                "type" : "IB",
                "distribution" : "ll",
                "lambda" : "df",
                "normalization" : "z",
                "normalization.z.z" : "0.25"
            }
        }
        "number_of_replicas": 1,
        "number_of_shards": 10
    },
    "mappings": {
        "_default_": {
          "_all": {
            "enabled": false
          },
          "_source": {
            "enabled": true
          }
        },
        "doc": {
            "properties": {
                "id": {"type": "text"},
                "title": {"type": "text","similarity": "my_bm25"},
                "official_title": {"type": "text","similarity": "my_bm25"},
                "summary": {"type": "text","similarity": "my_bm25"},
                "detailed_description": {"type": "text","similarity": "my_bm25"},
                "condition": {"type": "text","similarity": "my_bm25"},
                "exclusion": {"type": "text","similarity": "my_bm25"},
                "inclusion": {"type": "text","similarity": "my_bm25"},
                "meshTags": {"similarity": "my_bm25"},
                "keywords": {"type": "text","similarity": "my_bm25"},
                "sex": {"type": "text","similarity": "my_bm25"},
                "maximum_age": {"type": "long"},
                "minimum_age": {"type": "long"}
            }
        }
    }
}
}

'
curl -XGET 'localhost:9200/posts/_mapping?pretty'
