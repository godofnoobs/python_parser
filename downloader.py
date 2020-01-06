import requests


class Downloader:
    def __init__(self):
        self.req = requests

    def get_page_html(self, url):
        res = requests.get(url)
        if (res.status_code == 200):
            return res.text
        raise ConnectionError('Eror status code {}'.format(res.status_code))
