__author__ = 'IronMan'
from mail_parser import MailParser
import jsonpickle
import io
import nlp
import json
import es


def result_email(file_name):
    with io.open(file_name) as file:
        text = file.read()

    parser = MailParser(text)
    results = parser.parse_thread()
    question = results.question
    keywords = nlp.keywords_from_text(question.content)
    messages = nlp.compute_tf_idf(question, results.messages)
    results.messages = messages
    # print(results)

    # es.store_articles([question] + messages
    es.store_thread(results)

    for m in messages:
        print(jsonpickle.encode(m))


result_email("long.txt")
