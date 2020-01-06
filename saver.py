import os


class Saver:

    def make_dir(self, dir_path):
        if (not dir_path.is_dir()):
            os.mkdir(dir_path)

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
