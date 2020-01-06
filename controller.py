from pathlib import Path
from saver import Saver
from downloader import Downloader
from soup import Soup

default_params = {
    'dir_path': Path('./dist').resolve(),
    'base_url': 'https://tvoiraskraski.ru/%D0%B2%D1%81%D0%B5-%D1%80%D0%B0%D1%81%D0%BA%D1%80%D0%B0%D1%81%D0%BA%D0%B8',  # noqa: E501
    'base_html_path': Path('./dist/base.html').resolve(),
    'global_map_file': Path('./dist/global_map.csv').resolve()
}


class Controller:
    def __init__(self, params=default_params):
        self.params = params
        self.setup()
        self.do_smth()

    def setup(self):
        self.saver = Saver()
        self.dl = Downloader()
        self.parser = Soup()

    def do_smth(self):
        # create dist dir
        dir_path = self.params['dir_path']
        self.saver.make_dir(dir_path)

        # get base page html from hdd/url
        html = self.get_base_html(self.params['base_url'])

        # parse
        self.parser.create_soup(html)
        map = self.parser.get_base_map()

        global_map = self.get_global_pics_map(map)

        self.saver.save_obj_to_csv(global_map, self.params['global_map_file'])

    def get_base_html(self, url=None):
        base_html_file_path = self.params['base_html_path']
        if (not self.saver.is_file(base_html_file_path)):
            html = self.dl.get_page_html(url)
            self.saver.save_txt_to_file(html, base_html_file_path)
        else:
            html = self.saver.read_txt_file(base_html_file_path)
        return html

    def get_global_pics_map(self, map):
        global_map = []
        count = 1
        for meta_obj in map:
            print(count)
            html = self.get_pics_page(meta_obj)
            subcat_map = self.get_subcat_map(html, meta_obj)
            global_map = global_map + subcat_map
            count += 1
        return global_map

    def get_subcat_map(self, html, meta_obj):
        self.parser.create_soup(html)
        return self.parser.get_pics_map(meta_obj)

    def get_pics_page(self, rec):
        html = self.dl.get_page_html(rec['link'])
        return html
