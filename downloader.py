import requests
from PIL import Image, ImageFile
from io import BytesIO
ImageFile.LOAD_TRUNCATED_IMAGES = True


class Downloader:
    def __init__(self):
        self.req = requests

    def get_page_html(self, url):
        res = requests.get(url)
        if (res.status_code == 200):
            return res.text
        raise ConnectionError('Eror status code {}'.format(res.status_code))

    def get_pic(self, url):
        res = requests.get(url)
        try:
            image = Image.open(BytesIO(res.content))
        except Exception:
            print('Error on', url)
            return None
        return image
