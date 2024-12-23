from pyparsing import empty
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pymongo import MongoClient
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk import ngrams
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from utilities import clean_text, connect_database


class Indexer:
    def __init__(self, database_name, corpus_collection_name, index_collection_name):
        self.database_name = database_name
        self.corpus_collection_name = corpus_collection_name
        self.index_collection_name = index_collection_name


    def get_all_target_pages(self):
        db = connect_database(self.database_name)
        collection = db[self.corpus_collection_name]
        corpus = collection.find({"is_target": True})
        return corpus


    def get_doc_text(self, doc):
        bs = BeautifulSoup(doc['page_html'], 'html.parser')
        fac_staff_div = bs.find('div', class_='fac-staff')
        all_text = fac_staff_div.get_text(separator=' ', strip=True)
        return all_text


    def create_master_doc_text_and_url_lists(self, corpus):
        master_doc_list = list()
        master_url_list = list()
        for document_obj in corpus:
            text = self.get_doc_text(document_obj)
            cleaned_text = clean_text(text)
            if len(cleaned_text) > 1:
                master_doc_list.append(cleaned_text)
                master_url_list.append(document_obj['url'])
        return master_doc_list, master_url_list


    def create_inverted_index(self, master_doc_list, master_url_list):
        inverted_dict = dict()
        vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 3))
        tfidf_matrix = vectorizer.fit_transform(master_doc_list)
        terms = vectorizer.get_feature_names_out()
        idf_values = vectorizer.idf_
        term_idf_map = dict(zip(terms, idf_values))
        for doc_idx, url in enumerate(master_url_list):
            tfidf_scores = tfidf_matrix[doc_idx]
            term_scores = zip(terms, tfidf_scores.toarray().flatten())
            for term, score in term_scores:
                if score > 0:
                    if term not in inverted_dict:
                        inverted_dict[term] = {'idf': term_idf_map[term], 'records': []}
                    inverted_dict[term]['records'].append({'url': url, 'tfidf': score})
        return inverted_dict


    def create_db_inverted_index(self, database_connection, inverted_dict):
        collection = database_connection[self.index_collection_name]
        for term, data in inverted_dict.items():
            collection.update_one(
                {'term': term},
                {'$set': {'idf': data['idf'], 'records': data['records']}},
                upsert=True
            )


    def generate_complete_inverted_index(self):
        corpus = self.get_all_target_pages()
        master_doc_list, master_url_list = self.create_master_doc_text_and_url_lists(corpus)
        inverted_dict = self.create_inverted_index(master_doc_list, master_url_list)
        db = connect_database(self.database_name)
        self.create_db_inverted_index(db, inverted_dict)
