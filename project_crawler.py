from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from GroupProject.utilities import fetch_and_parse
from project_content_parser import Parser


class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.parser = Parser()


    def visit_link_and_gather_anchor_tags(self, link_to_visit):
        return self.parser.get_anchor_tags(link_to_visit)


    def create_list_of_raw_links(self, unfiltered_url_list):
        filtered_url_list = []
        for individual_url in unfiltered_url_list:
            url_string = individual_url.get('href')
            if url_string and url_string.endswith(('.html', '.shtml')):
                filtered_url_list.append(url_string)
        return filtered_url_list


    def construct_correct_urls(self, current_page_url, filtered_url_list):
        absolute_urls = []
        for href in filtered_url_list:
            if not href.startswith('http'):
                absolute_urls.append(urljoin(current_page_url, href))
            else:
                absolute_urls.append(href)
        return absolute_urls


    def generate_new_frontier_urls(self, current_link):
        anchor_tags = self.visit_link_and_gather_anchor_tags(current_link)
        raw_list = self.create_list_of_raw_links(anchor_tags)
        frontier = self.construct_correct_urls(current_link, raw_list)
        return frontier


    def get_html(self, some_url_link):
        bs = fetch_and_parse(some_url_link)
        if bs is not None:
            return bs.prettify()
        else:
            return ""


    def is_target_link_no_parse(self, current_link, link_to_find):
        return link_to_find in current_link


    def is_domain_page(self, link):
        return self.base_url in link


    def is_department_page(self, link):
        return self.base_url in link


    def insert_into_database(self, db_manager, link, page_html, is_target):
        doc_obj = dict()
        doc_obj['url'] = link
        doc_obj['page_html'] = page_html
        doc_obj['is_target'] = is_target
        db_manager.insert_document(doc_obj)


    def crawl(self, seed_url, db_manager, target_text_page_flag):
        base_frontier = self.generate_new_frontier_urls(seed_url)
        num_targets = 22
        targets_found = 0
        visited_urls = set()
        while base_frontier:
            link = base_frontier.pop(0)
            if link in visited_urls:
                continue
            visited_urls.add(link)
            if self.is_domain_page(link):
                is_target = self.parser.is_target_page(link, target_text_page_flag)
                if is_target:
                    targets_found += 1
                page_html = self.get_html(link)
                if page_html:
                    self.insert_into_database(db_manager, link, page_html, is_target)
                if targets_found == num_targets:
                    base_frontier.clear()
                    return
            additional_frontier = self.generate_new_frontier_urls(link)
            for next_link in additional_frontier:
                if next_link not in base_frontier:
                    base_frontier.append(next_link)
