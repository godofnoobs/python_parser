from bs4 import BeautifulSoup as bs
import gc

url = 'https://tvoiraskraski.ru'

default_params = {
    'base_div': '.views-content',
    'base_category': 'h3',
}


class Soup:
    def __init__(self, params=default_params):
        self.params = params

    def create_soup(self, html):
        if (hasattr(self, 'soup')):
            self.soup.decompose()
            self.soup = None
            gc.collect()
        self.soup = bs(html, 'html.parser')

    def get_base_map(self):
        el = self.soup.h3
        category = el.a.get_text()
        base_map = []
        while el.next_sibling:
            el = el.next_sibling
            if (el.name == 'h3'):
                category = el.a.get_text()
            elif (el.name == 'div'):
                rec = {
                    'category': category,
                    'subcategory': el.a.get_text(),
                    'link': url + el.a['href'],
                }
                base_map.append(rec)
        return base_map

    def get_pics_map(self, meta_obj):
        el = self.soup.figure
        subcat_map = []
        while True:
            if (hasattr(el, 'name') and el.name == 'figure'):
                rec = {
                    'category': meta_obj['category'],
                    'subcategory': meta_obj['subcategory'],
                    'link': el.a['href']
                }
                subcat_map.append(rec)
            if (not hasattr(el, 'name') or not el.next_sibling):
                break
            el = el.next_sibling
        return subcat_map
