import re
#from turtledemo.penrose import start

from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient
import pickle
import pprint

BLURP_WIDTH = 3 #how many words before and after query term


def clean_text(some_text):
    removed_punctuation = remove_punctuation(some_text)
    filtered_words = remove_stopwords(removed_punctuation)
    lemmas = lemmatize(filtered_words)
    text = " ".join(lemmas).lower().strip()
    cleaned_string = re.sub(r'\n', ' ', text)
    return cleaned_string

def remove_punctuation(some_text):
    return re.sub(r'[^\w\s]', '', some_text)

def remove_stopwords(some_text):
    split_text = word_tokenize(some_text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in split_text if word.lower() not in stop_words]
    return filtered_words

def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word, pos="n") for word in tokens]

def remove_nonfeature_words(some_text):
    terms = {}
    with open("terms_vocabulary.pkl", "rb") as f:
        terms = pickle.load(f)

    words = some_text.split()
    filtered_text = [word for word in words if terms.get(word) is not None]
    return ' '.join(filtered_text)
        

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


def show_formatted_results(query_string, ranked_result_list, database_name, db_collection_name):
    if ranked_result_list is not None:
        rank = 1
        for key, value in ranked_result_list:
            blurb = get_blurb(query_string, key, database_name, db_collection_name)
            print('(', rank, ') :', key)
            pprint.pprint(blurb)
            rank += 1
    else:
        print("Search did not return any results")


def get_blurb(query_string, url, database_name, db_collection_name):
    
    q_words = query_string.split()
    q_lemmas = clean_text(query_string).split()

    db = connect_database(database_name)
    col = db[db_collection_name]
    doc = col.find_one({"url": url})

    if doc is not None:
        bs = BeautifulSoup(doc['page_html'], 'html.parser')
    
    blurb = generate_blurb(q_lemmas, bs)
    if blurb is '':
        blurb = generate_blurb(q_words, bs)

    return blurb


def generate_blurb(words, bs):
    combined_blurb = ''
    for word in words:
        surround_regex = rf"(?:\S+\s){{0,{BLURP_WIDTH}}}\b{word}\b(?:\s\S+){{0,{BLURP_WIDTH}}}"
        body_text = bs.find('div', class_='fac-staff').get_text()
        blurp = re.search(surround_regex, body_text, flags=re.IGNORECASE)
        if blurp:
            combined_blurb += blurp.group() + '...'
        combined_blurb = combined_blurb.replace(u'\xa0', u' ')
    return combined_blurb


def take_user_query_input():
    query_string = input("Search: ")
    return query_string


