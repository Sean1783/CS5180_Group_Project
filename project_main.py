import pprint

from GroupProject.project_query_processor import QueryProcessor
from project_db_manager import DatabaseManager
from project_content_parser import *
from project_crawler import *
from project_indexer import Indexer


# This worked
database_name = 'project_db'
corpus_collection_name = 'v2_test_pages'
seed = 'https://www.cpp.edu/cba/international-business-marketing/index.shtml'
base_url = 'https://www.cpp.edu'
target_url = 'https://www.cpp.edu/faculty/'


def query_processor_demo():
    query_processor = QueryProcessor()
    query_string = "baby formula watchlist exercise community."
    results = query_processor.query_v2(query_string)
    ranked_results = query_processor.rank_result(results)
    query_processor.show_formatted_results(ranked_results)


def crawler_demo():
    crawler = Crawler(base_url, target_url)
    db_manager = DatabaseManager(database_name, corpus_collection_name)
    crawler.crawl(seed, db_manager)


def indexer_demo():
    indexer = Indexer(database_name, corpus_collection_name, 'v2_inverted_index')
    # target_pages = indexer.get_all_target_pages()
    # example_text = indexer.get_doc_text(target_pages[4])
    indexer.generate_complete_inverted_index()


if __name__ == "__main__":
    query_processor_demo()
    # crawler_demo()
    # indexer_demo()
