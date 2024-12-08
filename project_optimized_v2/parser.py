from urllib.request import urlopen
from db_connection_mongo import *
from bs4 import BeautifulSoup
from crawler import cleanURL
import re

def parse_faculty_profile(url, html):
    bs = BeautifulSoup(html, 'html.parser')
    
    fac_info = bs.find(attrs = { 'class': 'fac-info' })
    name = fac_info.find('h1')
    title_dept = fac_info.find('span', { 'class': 'title-dept' })
    contact_info = fac_info.find(attrs = { 'class': 'menu-left' })
    email = contact_info.find('a', href = lambda href: href and href.startswith('mailto:'))
    phone = contact_info.find('p', { 'class': 'phoneicon' })
    location_info = fac_info.find(attrs = { 'class': 'menu-right' })
    office = location_info.find('p', { 'class': 'locationicon' })
    hours = location_info.find('p', { 'class': 'hoursicon' })
    
    # Extract sections from main content
    sections = []
    main_content = bs.find(attrs = { 'class': 'fac-staff' })
    if main_content:
        blurbs = main_content.find_all(attrs = { 'class': 'blurb' })
        for blurb in blurbs:
            section_title = blurb.find('h2')
            section_content = blurb.find(attrs = { 'class': 'section-menu' })
            section = {
                'title': section_title.text.strip() if section_title else '',
                'content': section_content.text.strip() if section_content else ''
            }
            sections.append(section)
    
    
    # Extract navigation links
    nav_links = []
    left_nav = bs.find(attrs = { 'class': 'fac-nav' })
    if left_nav:
        links = left_nav.find_all('a')
        nav_links = [{'text': link.text.strip(), 'href': cleanURL(url, link.get('href', ''))} for link in links]
        nav_links = [link for link in nav_links if not link['href'] == url]
    
    
    # Extract accolades
    accolades = []
    right_col = bs.find('aside', { 'class': 'fac rightcol' })
    if right_col:
        accolade_section = right_col.find(attrs = { 'class': 'accolades' })
        if accolade_section:
            accolade_title = accolade_section.find('h2')
            accolade_content = accolade_section.findNextSiblings()
            accolades.append({
                'title': accolade_title.text.strip() if accolade_title else '',
                'content': [content.text.strip() for content in accolade_content]
            })
    
    return {
        'name': name.text.strip() if name else '',
        'title_department': title_dept.text.strip() if title_dept else '',
        'email': email.text.strip() if email else '',
        'phone': phone.text.strip() if phone else '',
        'office': office.text.strip() if office else '',
        'office_hours': hours.text.strip() if hours else '',
        'sections': sections,
        'navigation_links': nav_links,
        'accolades': accolades
    }


if __name__ == '__main__':
    db = connectDataBase()
    pages = db["pages"]
    professors = db["professors"]
    professors.drop()

    targetPages = findPages(pages, { "target": True })
    if not targetPages:
        print("No target page found... Run crawler.py to retrieve target page.")
        exit(0)
    
    for targetPage in targetPages:
        url = targetPage["url"]
        html = targetPage["html"]
        professor_profile = parse_faculty_profile(url, html)
        addProfessor(professors, **professor_profile)