from pathlib import Path, PurePath
from nanoid import generate
from saver import Saver
from downloader import Downloader
from soup import Soup

default_params = {
    'dir_path': Path('./dist/').resolve(),
    'img_path': Path('./dist/img/').resolve(),
    'img_min_path': Path('./dist/img_min/').resolve(),
    'base_url': 'https://tvoiraskraski.ru/%D0%B2%D1%81%D0%B5-%D1%80%D0%B0%D1%81%D0%BA%D1%80%D0%B0%D1%81%D0%BA%D0%B8',  # noqa: E501
    'base_html_path': Path('./dist/base.html').resolve(),
    'global_map_file': Path('./dist/global_map.csv').resolve(),
    'downloaded_map_file': Path('./dist/downloaded_map.csv').resolve(),
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

    def get_stored_map(self, path, sep='::'):
        schema = ['category', 'subcategory', 'link']
        res_map = self.saver.read_csv_file(
            path,
            schema,
            sep
        )
        return list(res_map)

    def get_target_map(self):
        schema = ['category', 'subcategory', 'link']
        sep = '::'
        global_map = list(self.saver.read_csv_file(
            self.params['global_map_file'],
            schema,
            sep
        ))
        if (not self.saver.is_file(self.params['downloaded_map_file'])):
            return global_map
        downloaded_map = list(self.saver.read_csv_file(
            self.params['downloaded_map_file'],
            schema,
            sep
        ))
        target_map = []
        for it1 in global_map:
            for it2 in downloaded_map:
                if (
                    it1['category'] == it2['category'] and
                    it1['subcategory'] == it2['subcategory'] and
                    it1['link'] == it2['link']
                ):
                    break
            else:
                target_map.append(it1)
        return target_map

    def download_all_pics(self):
        # create dist dirs
        dir_path = self.params['img_path']
        self.saver.make_dir(dir_path)
        dir_path = self.params['img_min_path']
        self.saver.make_dir(dir_path)

        target_map = self.get_target_map()
        for item in target_map:
            name = self.download_pic(item['link'])
            if (name):
                item['name'] = name
                dir_path = self.params['downloaded_map_file']
                self.saver.append_obj_to_csv(item, dir_path)

    def get_minified_image(self, image):
        new_width = 120
        new_height = int(round(120 * image.height / image.width))
        min_image = image.resize((new_width, new_height))
        return min_image

    def download_pic(self, url=None):
        try:
            image = self.dl.get_pic(url)
            if (not image):
                return None
            min_image = self.get_minified_image(image)
            res_type = '.jpg' if (url.split('.')[-1] in ['jpg', 'jpeg']) else '.png'  # noqa501
            name = generate() + res_type
            path = Path(PurePath(self.params['img_path']).joinpath(name))
            min_path = Path(PurePath(self.params['img_min_path']).joinpath(name))  # noqa501
            self.saver.save_image(image, path)
            self.saver.save_image(min_image, min_path)
        except Exception:
            print('Error on', url, name)
            self.saver.remove_file(path)
            self.saver.remove_file(min_path)
            return None
        return name

    def grab_global_map(self):
        # create dist dirs
        dir_path = self.params['dir_path']
        self.saver.make_dir(dir_path)

        # get base page html from hdd/url
        html = self.get_base_html(self.params['base_url'])

        # parse
        self.parser.create_soup(html)
        base_map = self.parser.get_base_map()

        # get global map of all pics and store it into csv file
        global_map = self.get_global_pics_map(base_map[:50])
        self.saver.save_obj_to_csv(global_map, self.params['global_map_file'])

    def do_smth(self):
        if (not self.saver.is_file(self.params['global_map_file'])):
            self.grab_global_map()
        self.download_all_pics()

    def get_base_html(self, url=None):
        base_html_file_path = self.params['base_html_path']
        if (not self.saver.is_file(base_html_file_path)):
            html = self.dl.get_page_html(url)
            self.saver.save_txt_to_file(html, base_html_file_path)
        else:
            html = self.saver.read_txt_file(base_html_file_path)
        return html

    def get_global_pics_map(self, base_map):
        global_map = []
        for meta_obj in base_map:
            html = self.get_pics_page(meta_obj)
            subcat_map = self.get_subcat_map(html, meta_obj)
            global_map = global_map + subcat_map
        return global_map

    def get_subcat_map(self, html, meta_obj):
        self.parser.create_soup(html)
        return self.parser.get_pics_map(meta_obj)

    def get_pics_page(self, rec):
        html = self.dl.get_page_html(rec['link'])
        return html
