from flask import Flask
from elasticsearch import Elasticsearch

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/search/<query_words>')
def search(query_words):
    client = Elasticsearch()

    response = client.search(
        index="posts",
        body={
            "query": {
                 "match" : {
                     "topic": {
                        "query": query_words,
                        "operator": "or",
                        "boost": 3
                     }
                },
                "match" : {
                    "question.key_words": {
                        "query": query_words,
                        "operator": "or",
                        "boost": 2
                    }
                }
            }
        }
     })




if __name__ == '__main__':
    app.run()
