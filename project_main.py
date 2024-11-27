import pprint

from GroupProject.project_indexer import Indexer
from GroupProject.project_query_processor import QueryProcessor
from project_db_manager import DatabaseManager
from project_content_parser import *
from project_crawler import *
from project_indexer import Indexer


# This works to find all professor pages.
database_name = 'project_db'
# web_crawler_collection_name = 'project_pages'
web_crawler_collection_name = 'v2_test_pages'
# professor_info_collection_name = 'project_professors'
seed = 'https://www.cpp.edu/cba/international-business-marketing/index.shtml'
# base_url = 'https://www.cpp.edu'
base_url = 'https://www.cpp.edu/cba/international-business-marketing/'
target_url = 'https://www.cpp.edu/faculty/'
# target_url = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'

def query_processor_test():
    query_processor = QueryProcessor()
    query_processor.query()


def crawler_test():
    crawler = Crawler(base_url, target_url)
    db_manager = DatabaseManager(database_name, web_crawler_collection_name)
    crawler.crawl(seed, db_manager)


def indexer_test():
    indexer = Indexer()
    indexer.generate_complete_inverted_index()


if __name__ == "__main__":
    query_processor_test()
    # indexer_test()
    # crawler_test()
    # parser_test()