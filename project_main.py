import pprint

from GroupProject.project_indexer import Indexer, clean_text
from GroupProject.project_query_processor import QueryProcessor
from project_db_manager import DatabaseManager
from project_content_parser import *
from project_crawler import *
from project_indexer import Indexer


# # This works to find all professor pages.
# database_name = 'project_db'
# # web_crawler_collection_name = 'project_pages'
# web_crawler_collection_name = 'v2_test_pages'
# # professor_info_collection_name = 'project_professors'
# seed = 'https://www.cpp.edu/cba/international-business-marketing/index.shtml'
# # base_url = 'https://www.cpp.edu'
# base_url = 'https://www.cpp.edu/cba/international-business-marketing/'
# target_url = 'https://www.cpp.edu/faculty/'
# # target_url = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'


# This worked
database_name = 'project_db'
web_crawler_collection_name = 'v2_test_pages'
seed = 'https://www.cpp.edu/cba/international-business-marketing/index.shtml'
base_url = 'https://www.cpp.edu'
# base_url = 'https://www.cpp.edu/cba/international-business-marketing/'
target_url = 'https://www.cpp.edu/faculty/'
# target_url = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'


def query_processor_demo():
    query_processor = QueryProcessor()
    query_processor.query()


def crawler_demo():
    crawler = Crawler(base_url, target_url)
    db_manager = DatabaseManager(database_name, web_crawler_collection_name)
    crawler.crawl(seed, db_manager)


def indexer_demo():
    indexer = Indexer('project_db', 'v2_test_pages', 'v2_inverted_index')
    # target_pages = indexer.get_all_target_pages()
    # example_text = indexer.get_doc_text(target_pages[4])
    indexer.generate_complete_inverted_index()


if __name__ == "__main__":
    # query_processor_test()
    crawler_demo()
    indexer_demo()
    # parser_test()