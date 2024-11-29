import pprint

from project_query_processor import QueryProcessor
from utilities import take_user_query_input
from utilities import clean_text, connect_database, show_formatted_results
from project_db_manager import DatabaseManager
from project_content_parser import *
from project_crawler import *
from project_indexer import Indexer


# This worked
database_name = 'project_db'
corpus_collection_name = 'v2_test_pages'
# corpus_collection_name = 'v3_test_pages'
seed = 'https://www.cpp.edu/cba/international-business-marketing/index.shtml'
base_url = 'https://www.cpp.edu'
target_url = 'https://www.cpp.edu/faculty/'


def query_processor_demo():
    query_processor = QueryProcessor()
    print("Enter \':q\' to quit")
    while True:
        query_string = take_user_query_input()
        if query_string == ':q':
            break
        results = query_processor.query_v2(query_string)
        ranked_results = query_processor.rank_result(results)
        show_formatted_results(query_string, ranked_results, database_name)


def crawler_demo():
    crawler = Crawler(base_url, target_url)
    db_manager = DatabaseManager(database_name, corpus_collection_name)
    crawler.crawl(seed, db_manager)


def indexer_demo():
    indexer = Indexer(database_name, corpus_collection_name, 'v2_inverted_index')
    # indexer = Indexer(database_name, corpus_collection_name, 'v3_inverted_index')
    indexer.generate_complete_inverted_index()


if __name__ == "__main__":
    #crawler_demo()
    #indexer_demo()
    query_processor_demo()

