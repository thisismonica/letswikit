__author__ = 'IronMan'

from elasticsearch import Elasticsearch
import uuid

es = Elasticsearch()


def store_articles(articles):
    for a in articles:
        d = a.json()
        print(d)
        id = uuid.uuid4()
        es.index(index="test", doc_type="article", body=d, id=id)


def store_thread(thread):
    d = thread.json()
    print(d)
    id = uuid.uuid4()
    es.index(index="test3", doc_type="article", body=d, id=id)

