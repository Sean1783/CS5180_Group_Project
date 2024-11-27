#Convert a collection of text documents to a matrix of token counts.
import pprint
import string

from pyparsing import empty
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pymongo import MongoClient
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk import ngrams


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

def clean_text(some_text):
    split_text = some_text.split()
    cleaned_string = ""
    for word in split_text:
        if len(word) > 0:
            if word[len(word) - 1] == '.':
                word = word[:-1]
            elif word[len(word) - 1] == ',':
                word = word[:-1]
            word = word.lower()
            word = word.replace('\xa0', ' ')
            cleaned_string += word + " "
    # cleaner_text = some_text.lower()
    # cleaner_text = cleaner_text.replace('\n', '')
    # cleaner_text = cleaner_text.replace('.', ' ')
    return cleaned_string


db = connectDataBase()
collection = db.project_pages
corpus = collection.find({"is_target" : True})

inverted_dict = dict()

master_doc_list = list()
master_url_list = list()
for document_obj in corpus:
    bs = BeautifulSoup(document_obj['page_html'], 'html.parser')
    p_tags = bs.main.find_all('p')
    full_text = []
    for element in p_tags:
        cleaned_text = clean_text(element.text)
        if len(cleaned_text) > 1:
            full_text.append(cleaned_text)
            master_doc_list.append(cleaned_text)
            master_url_list.append(document_obj['url'])

vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 3))
tfidf_matrix = vectorizer.fit_transform(master_doc_list)
terms = vectorizer.get_feature_names_out()

# Unneeded if collection has already been created.
for doc_idx, url in enumerate(master_url_list):
    tfidf_scores = tfidf_matrix[doc_idx]  # TF-IDF scores for this document
    term_scores = zip(terms, tfidf_scores.toarray().flatten())
    for term, score in term_scores:
        if score > 0:  # Only store terms with non-zero TF-IDF scores
            if term not in inverted_dict:
                inverted_dict[term] = []  # Initialize list for this term
            inverted_dict[term].append({'url': url, 'tfidf': score})
#
# collection = db.inverted_index
# for term, records in inverted_dict.items():
#     print(term, records)
#     collection.update_one(
#         {'term': term},
#         {'$set': {'records': records}},
#         upsert=True
#     )


query_string = "swimming snowboarding"
query_string = clean_text(query_string)
vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 3))
res = vectorizer.fit([query_string])  # Fit the query text
ngrams = vectorizer.get_feature_names_out()
collection = db.inverted_index

print(vectorizer.vocabulary_)

hits = dict()
for ngram in ngrams:
    result = collection.find_one({'term' : ngram})
    if result:
        term = result['term']
        for doc in result['records']:
            url = doc["url"]
            score = doc["tfidf"]
            if url in hits:
                hits[url] += score
            else:
                hits[url] = score

print(hits)

    # combined_text = " ".join(full_text)
    # vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 3))
    # vectorizer.fit([combined_text])
    # for term in vectorizer.vocabulary_:
    #     if term not in inverted_dict:
    #         doc_list = list()
    #         doc_list.append(current_url)
    #         inverted_dict[term] = doc_list
    #     else:
    #         inverted_dict[term].append(current_url)

# print(inverted_dict)


# for key, value in inverted_dict.items():
#     db_entry = dict()
#     db_entry['term'] = key
#     db_entry[key] = value
#     collection.insert_one(db_entry)


# doc_obj = dict()
# doc_obj['url'] = link
# doc_obj['page_html'] = page_html
# doc_obj['is_target'] = is_target
# db_manager.insert_document(doc_obj)


# p_tag_element = p_tags[10]

# One <p> element's text converted to a list.
# p_tag_element_list = [p_tags[10].get_text()]

# Generating n-grams
# vectorizer = CountVectorizer(analyzer='word', ngram_range = (1, 4))
# for element in p_tags:
#     element_text = [element.get_text()]
#     vectorizer.fit(element_text)
    # print(vectorizer.vocabulary_)
    # vector = vectorizer.transform(element_text)
    # print(vector.shape)
    # print(vector.toarray())

# vectorizer = TfidfVectorizer(ngram_range = (1, 4))
# documents = ["On the other hand, this one is about cats. Everyone loves cats.",
#                 "This document is about dogs. I love dogs.",
#                 "But there are others that are about things completely unknown. Like surfing."]
# # vectorizer.fit(search_query)
# result = vectorizer.fit_transform(documents)
# print(result)
# display = result.toarray()
# for row in display:
#     print(row)
# print(vectorizer.vocabulary_)


documents = ["On the other hand, this one is about cats. Everyone loves cats.",
                "This document is about dogs. I love dogs.",
                "But there are others that are about things completely unknown. Like surfing."]

# documents = ["The dogs slept behind the churches", "The dogs churches."]
# vectorizer = CountVectorizer(analyzer='word', ngram_range = (1, 1))
# doc_term_matrix = vectorizer.fit_transform(text)
# print("(doc#, pos) count")
# print(doc_term_matrix)

# inverted_matrix = dict()
# for i in range(len(documents)):
#     for word in documents[i].split():
#         if word not in inverted_matrix:
#             doc_list = list()
#             doc_list.append(i)
#             inverted_matrix[word] = doc_list
#         else:
#             inverted_matrix[word].append(i)
# print(inverted_matrix)



# vector = vectorizer.transform(documents)
#
# print(vector.shape)
# print(vector.toarray())









# result = vectorizer.transform(search_query)
# print(result)


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
