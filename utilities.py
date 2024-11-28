import re
from turtledemo.penrose import start

from bs4 import BeautifulSoup
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


def generate_results_blurb(query_string, ranked_results, db_collection_name):
    db = connect_database(db_collection_name)
    for key, value in ranked_results:
        url = value
        doc = db.find_one({"url": url})
        # Get the relevant record for the url.
        if doc is not None:
            bs = BeautifulSoup(doc['page_html'], 'html.parser')
            fac_staff_div = bs.find('div', class_='fac-staff')
            # Get all the text from this web page.
            all_text = fac_staff_div.get_text(separator=' ', strip=True)
            all_text_length = len(all_text)
            # Loop through every word in the query string.
            for word in query_string.split():
                starting_index = all_text.find(word)
                if starting_index != -1:
                    prefix = ""
                    suffix = ""
                    stop_idx = starting_index + len(word)
                    while stop_idx < stop_idx + 10 and stop_idx < len(all_text):
                        suffix += all_text[stop_idx]
                        stop_idx += 1
                    start_idx = starting_index
                    while start_idx >= 0 and start_idx > starting_index - 10:
                        prefix += all_text[start_idx]
                        start_idx -= 1
                    prefix += word + suffix



def take_user_query_input():
    query_string = input("Search: ")
    return query_string


