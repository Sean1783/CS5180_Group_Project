from bs4 import BeautifulSoup
import re


class Parser:


    def extract_info(self, page_url, db_manager):
        content_string = db_manager.get_document_html(page_url)
        profile_info = list()
        if not content_string or 'page_html' not in content_string:
            return None

        try:
            bs = BeautifulSoup(content_string['page_html'], 'html.parser')
            target_objects = bs.find('div', id='main')
            if target_objects is None:
                return None

            h2_tags = target_objects.find_all('h2')
            for h2 in h2_tags:
                p_tag = h2.find_next_sibling('p')
                name = h2.get_text().strip()
                email = self.alt_extract_email(p_tag)
                websites = self.alt_extract_website(p_tag)
                current_profile = dict()
                current_profile['Name'] = name
                current_profile['Email'] = email
                current_profile['Website'] = websites[0] if len(websites) > 0 else None
                stats = self.extract_stats(p_tag)
                combined_profile = {**current_profile, **stats}
                profile_info.append(combined_profile)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        return profile_info


    def extract_stats(self, p_tag):
        additional_details = p_tag.find_all('strong')
        current_profile = dict()
        for detail in additional_details:
            category = detail.get_text().strip()
            if re.match(r'^Email.*', category):
                pass
            elif re.match(r'^Web:?', category):
                pass
            else:
                key = re.sub(r'[^\w]', '', category)
                value = detail.next_sibling.strip()
                current_profile[key] = value
        return current_profile


    def alt_extract_email(self, current_obj):
        email_pattern = r'[a-zA-Z0-9._%+-]+@cpp\.edu'
        email = []
        try:
            text = current_obj.get_text()
            email = re.findall(email_pattern, text)
            return email[0]
        except Exception as e:
            print(e)
        return email


    def alt_extract_website(self, current_obj):
        website_pattern = r'https?'
        a_tags = current_obj.find_all('a', href=True)
        websites = []
        for a_tag in a_tags:
            href = a_tag['href']
            if re.match(website_pattern, href):
                websites.append(href)
        return websites


    def extract_email(self, current_obj):
        p_tag = current_obj.find('p')
        email_pattern = r'[a-zA-Z0-9._%+-]+@cpp\.edu'
        email = []
        try:
            p_text = p_tag.get_text()
            email = re.findall(email_pattern, p_text)
            return email[0]
        except Exception as e:
            print(e)
        return email


    def extract_website(self, current_obj):
        website_pattern = r'https?'
        p_tag = current_obj.find('p')
        a_tags = p_tag.find_all('a', href=True)
        websites = []
        for a_tag in a_tags:
            href = a_tag['href']
            if re.match(website_pattern, href):
                websites.append(href)
        return websites
