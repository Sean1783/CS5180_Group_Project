import pprint
import time

from GroupProject.project_query_processor import QueryProcessor
from GroupProject.utilities import take_user_query_input
from utilities import clean_text, connect_database, show_formatted_results
from project_db_manager import DatabaseManager
from project_content_parser import *
from project_crawler import *
from project_indexer import Indexer


database_name = 'project_db'
# corpus_collection_name = 'v2_test_pages'
corpus_collection_name = 'v3_test_pages'
# inverted_index_collection_name = 'v2_inverted_index'
inverted_index_collection_name = 'v3_inverted_index'
seed = 'https://www.cpp.edu/cba/international-business-marketing/index.shtml'
base_url = 'https://www.cpp.edu'


def crawler_demo():
    crawler = Crawler(base_url)
    db_manager = DatabaseManager(database_name, corpus_collection_name)
    target_text_page_flag = "Business"
    crawler.crawl(seed, db_manager, target_text_page_flag)


def indexer_demo():
    indexer = Indexer(database_name, corpus_collection_name, inverted_index_collection_name)
    indexer.generate_complete_inverted_index()


def query_processor_demo():
    query_processor = QueryProcessor(database_name, inverted_index_collection_name)
    print("Enter \':q\' to quit")
    while True:
        query_string = take_user_query_input()
        if query_string == ':q':
            break
        results = query_processor.query_v2(query_string)
        ranked_results = query_processor.rank_result(results)
        show_formatted_results(query_string, ranked_results, database_name, corpus_collection_name)


if __name__ == "__main__":
    start_crawler_time = time.time()
    crawler_demo()
    end_crawler_time = time.time()
    print('crawler elapsed time:', end_crawler_time - start_crawler_time)
    indexer_demo()
    end_indexer_time = time.time()
    print('indexer elapsed time:', end_indexer_time - end_crawler_time)
    query_processor_demo()

