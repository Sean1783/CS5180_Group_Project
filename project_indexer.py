from pyparsing import empty
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pymongo import MongoClient
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk import ngrams
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def clean_text(some_text):
    split_text = word_tokenize(some_text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in split_text if word.lower() not in stop_words]
    text = " ".join(filtered_words).lower()
    cleaned_string = re.sub(r'[^\w\s]', '', text)
    return cleaned_string


def connect_database():
    DB_NAME = "project_db"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")


class Indexer:


    def get_all_target_pages(self):
        db = connect_database()
        collection = db.v2_test_pages
        corpus = collection.find({"is_target": True})
        return corpus


    # Grabs relevant text from pages.
    # This will need data cleaning - clean '.', ',', etc.
    def create_master_doc_text_and_url_lists(self, corpus):
        master_doc_list = list()
        master_url_list = list()
        for document_obj in corpus:
            bs = BeautifulSoup(document_obj['page_html'], 'html.parser')
            p_tags = bs.main.find_all('p')
            # full_text = []
            for element in p_tags:
                cleaned_text = clean_text(element.text)
                if len(cleaned_text) > 1:
                    # full_text.append(cleaned_text)
                    master_doc_list.append(cleaned_text)
                    master_url_list.append(document_obj['url'])
        return master_doc_list, master_url_list


    def create_inverted_index(self, master_doc_list, master_url_list):
        inverted_dict = dict()
        vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 3))
        tfidf_matrix = vectorizer.fit_transform(master_doc_list)
        terms = vectorizer.get_feature_names_out()
        for doc_idx, url in enumerate(master_url_list):
            tfidf_scores = tfidf_matrix[doc_idx]
            term_scores = zip(terms, tfidf_scores.toarray().flatten())
            for term, score in term_scores:
                if score > 0:
                    if term not in inverted_dict:
                        inverted_dict[term] = []
                    inverted_dict[term].append({'url': url, 'tfidf': score})
        return inverted_dict


    def create_db_inverted_index(self, inverted_dict):
        db = connect_database()
        # Need a better way to reference the correct collection.
        collection = db.v2_inverted_index
        for term, records in inverted_dict.items():
            collection.update_one(
                {'term': term},
                {'$set': {'records': records}},
                upsert=True
            )


    def generate_complete_inverted_index(self):
        corpus = self.get_all_target_pages()
        master_doc_list, master_url_list = self.create_master_doc_text_and_url_lists(corpus)
        inverted_dict = self.create_inverted_index(master_doc_list, master_url_list)
        self.create_db_inverted_index(inverted_dict)
