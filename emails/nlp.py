__author__ = 'IronMan'

from nltk import word_tokenize
from nltk import pos_tag
from nltk import sent_tokenize
import re
from nltk.text import Text
from nltk.text import TextCollection

keywords_tags = ['FW', 'JJ', 'JJS', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def keywords_from_sentence(sentence):
    tags = pos_tag(sentence)
    keywords = []
    for tag in tags:
        token = tag[0]
        pos = tag[1]
        token = re.sub(r'[^\w\s]', '', token)
        if len(token) > 3 and pos in keywords_tags:
            keywords.append(token)
    return keywords


def keywords_from_text(text):
    sentences = sent_tokenize(text)
    keywords = []
    for sentence in sentences:
        keywords += keywords_from_sentence(word_tokenize(sentence))
    return list(set(keywords))


def compute_tf_idf(question, messages):
    import math

    texts = [question.keywords]
    total_length = 0
    for m in messages:
        total_length += len(m.keywords)
        text = Text(tokens=m.keywords)
        texts.append(text)
    text_collection = TextCollection(texts)
    question_tfidf_score = 0
    for k in question.keywords:
        tf_idf = text_collection.tf_idf(k, texts[0])
        question_tfidf_score += tf_idf

    if question_tfidf_score == 0:
        question_tfidf_score = 0.2
    if total_length == 0:
        total_length = 1
    length_factor = len(question.keywords) / total_length
    score = length_factor * math.log2(question_tfidf_score * 10)
    base_score = score
    if base_score == 0:
        base_score = 1

    print(question.content, question_tfidf_score, length_factor, score)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^")
    scores = []
    total_score = score
    print("Math", math)
    for i in range(0, len(messages)):
        tf_idf_i = 0
        for k in messages[i].keywords:
            tf_idf = text_collection.tf_idf(k, texts[i + 1])
            tf_idf_i += tf_idf
        if tf_idf_i == 0:
            continue
        length_factor = len(messages[i].keywords) / total_length
        score = length_factor * math.log2(tf_idf_i * 10)
        scores.append(score)
        total_score += score
        print(messages[i].content, tf_idf_i, length_factor, score)
        print("++++++++++++++++++++++++++++++++")
        # print(scores)
    averaged_scores = []
    last_message = question
    results = [last_message]
    for i in range(0, len(scores)):
        averaged_score = scores[i] / base_score
        averaged_scores.append(averaged_score)
        if averaged_score < 0.52:
            last_message.comments.append(messages[i])
        else:
            last_message = messages[i]
            results.append(last_message)
    print(averaged_scores)
    return results
