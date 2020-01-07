import os


class Saver:

    def make_dir(self, dir_path):
        if (not dir_path.is_dir()):
            os.mkdir(dir_path)

    def remove_file(self, file_path):
        if (self.is_file(file_path)):
            os.remove(file_path)

    def is_file(self, file_path):
        return file_path.is_file()

    def save_txt_to_file(self, txt, path):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(txt)
            file.close()

    def save_obj_to_csv(self, obj, path):
        def map_func(rec):
            res = rec['category'] + '::' + rec['subcategory'] + '::' + rec['link'] + '\n'  # noqa E501
            return res
        with open(path, 'w', encoding='utf-8') as file:
            file.writelines(map(map_func, obj))
            file.close()

    def read_txt_file(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            res = file.read()
            file.close()
        return res

    def read_csv_file(self, path, schema, sep=','):
        # schema is an array with text names of result object keys
        # in order of csv file data format
        def map_func(txt):
            txt = txt.rstrip('\n')
            arr = txt.split(sep)
            res_obj = {}
            for ind in range(len(schema)):
                res_obj[schema[ind]] = arr[ind]
            return res_obj
        with open(path, 'r', encoding='utf-8') as file:
            downloaded_map = map(map_func, file.readlines())
            file.close()
        return downloaded_map

    def save_image(self, image_obj, path):
        image_obj.save(path)

    def append_obj_to_csv(self, obj, path):
        txt = obj['category'] + '::' + obj['subcategory'] + '::' + obj['link'] + '::' + obj['name'] + '\n'  # noqa E501
        with open(path, 'a', encoding='utf-8') as file:
            file.write(txt)
            file.close()
