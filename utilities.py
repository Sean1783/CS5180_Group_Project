import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

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


def get_html(some_url_link):
    try:
        with urlopen(some_url_link) as html:
            return html.read()
    except HTTPError as e:
        print(f"HTTP error: {e}" + some_url_link)
    except URLError as e:
        print(f"URL error: {e}" + some_url_link)
    except Exception as e:
        print(f"An unexpected error occurred: {e}" + some_url_link)
    return ""


def fetch_and_parse(url):
    try:
        with urlopen(url) as response:
            return BeautifulSoup(response.read(), 'html.parser')
    except HTTPError as e:
        print(f"HTTP error: {e} - {url}")
    except URLError as e:
        print(f"URL error: {e} - {url}")
    except Exception as e:
        print(f"An unexpected error occurred: {e} - {url}")
    return None


def show_formatted_results(ranked_result_list, query_string, db_collection_name):
    if ranked_result_list is not None:
        rank = 1
        for key, value in ranked_result_list:
            print('(', rank, ') :', key)
            blurb = generate_results_blurb(query_string, ranked_result_list, db_collection_name)
            print(blurb)
            rank += 1
    else:
        print("Search did not return any results")


def generate_results_blurb(query_string, ranked_results, db_collection_name):
    db = connect_database('project_db')[db_collection_name]
    # print(ranked_results)
    for key, value in ranked_results:
        url = value
        doc = db.find_one({"url": url})
        if doc is not None:
            bs = BeautifulSoup(doc['page_html'], 'html.parser')
            fac_staff_div = bs.find('div', class_='fac-staff')
            all_text = fac_staff_div.get_text(separator=' ', strip=True)
            all_text_length = len(all_text)
            for word in query_string.split():
                starting_index = all_text.find(word)
                if starting_index != -1:
                    prefix = ""
                    suffix = ""
                    stop_idx = starting_index + len(word)
                    while stop_idx < stop_idx + 10 and stop_idx < all_text_length:
                        stop_idx += 1
                    start_idx = starting_index
                    while start_idx >= 0 and start_idx > starting_index - 10:
                        start_idx -= 1
                    prefix += word + suffix
                    return '...' + all_text[start_idx:stop_idx] + '...'



def take_user_query_input():
    query_string = input("Search: ")
    return query_string


