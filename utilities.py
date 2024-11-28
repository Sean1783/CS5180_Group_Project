import re

from nltk import word_tokenize
from nltk.corpus import stopwords
from pymongo import MongoClient


def clean_text(some_text):
    removed_punctuation = re.sub(r'[^\w\s]', '', some_text)
    split_text = word_tokenize(removed_punctuation)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in split_text if word.lower() not in stop_words]
    text = " ".join(filtered_words).lower().strip()
    cleaned_string = re.sub(r'\n', ' ', text)
    return cleaned_string


def connect_database(database_name):
    DB_NAME = database_name
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")


def show_formatted_results(ranked_result_list):
    if ranked_result_list is not None:
        rank = 1
        for key, value in ranked_result_list:
            print('(', rank, ') :', key)
            rank += 1
    else:
        print("Search did not return any results")

def take_user_query_input():
    query_string = input("Search: ")
    return query_string