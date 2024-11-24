#Convert a collection of text documents to a matrix of token counts.
from sklearn.feature_extraction.text import CountVectorizer
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import numpy as np
import pprint

def connectDataBase():
    DB_NAME = "project_db"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")

db = connectDataBase()
collection = db.project_pages

# doc = collection.find_one({"url" : "https://www.cpp.edu/privacy.shtml"})
doc = collection.find_one({"url" : "https://www.cpp.edu/faculty/mmulyanto/index.shtml"})
bs = BeautifulSoup(doc['page_html'], 'html.parser')
p_tags = bs.find_all('p')
# p_tag_element = p_tags[10]

# One <p> element's text converted to a list.
# p_tag_element_list = [p_tags[10].get_text()]

# Generating n-grams
vectorizer = CountVectorizer(analyzer='word', ngram_range = (1, 2))
for element in p_tags:
    element_text = [element.get_text()]
    vectorizer.fit(element_text)
    print(vectorizer.vocabulary_)
    # vector = vectorizer.transform(element_text)
    # print(vector.shape)
    # print(vector.toarray())


# vectorizer = CountVectorizer(analyzer='word', ngram_range = (1, 2))
# vectorizer.fit(p_tag_element_list)
#
# print(vectorizer.vocabulary_)
#
# vector = vectorizer.transform(p_tag_element_list)
#
# print(vector.shape)
# print(vector.toarray())




#
# # list of text documents
# text = ["The dogs slept behind the churches"]
#
# vectorizer = CountVectorizer(analyzer='word', ngram_range = (1, 2))
# vectorizer.fit(text)
#
# print(vectorizer.vocabulary_)
#
# vector = vectorizer.transform(text)
#
# print(vector.shape)
# print(vector.toarray())
