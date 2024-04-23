from unrar import rarfile
from zipfile import ZipFile
from tqdm import tqdm, trange
from itertools import product
import py7zr


class RndUnpack():
    upper_limit = 8
    lib_speical = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    lib_number = "1234567890"
    lib_upper_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lib_lower_letter = "abcdefghijklmnopqrstuvwxyz"
    lib_runtime = ""
    include_upper_letter = True
    include_lower_letter = True
    include_number = True
    include_speical = False

    def __init__(self, include_upper_letter=True, include_lower_letter=True, include_number=True, include_speical=False) -> None:
        self.include_upper_letter = include_upper_letter
        self.include_lower_letter = include_lower_letter
        self.include_number = include_number
        self.include_speical = include_speical

        if include_upper_letter:
            self.lib_runtime = self.lib_runtime + self.lib_upper_letter

        if include_lower_letter:
            self.lib_runtime = self.lib_runtime + self.lib_lower_letter

        if include_number:
            self.lib_runtime = self.lib_runtime + self.lib_number

        if include_speical:
            self.lib_runtime = self.lib_runtime + self.lib_speical

        print("Random password by:" + self.lib_runtime)

    def generate_passwords(self, n) -> list:
        # 使用itertools.product生成所有可能的排列组合
        passwords = [''.join(combination)
                     for combination in product(self.lib_runtime, repeat=n)]
        return passwords

    def attack_rar(self, file_path, max_count):
        if max_count <= 1:
            print("max_count must greater than 1")
        elif max_count > 16:
            print("max_count must less than 16")

        print("WARRNING: max_count could not be so large, else will time-consuming")

        for i in trange(1, max_count):
            li = self.generate_passwords(i)
            tbar = tqdm(li)
            for pwd in tbar:
                tbar.set_description('Processing ' + pwd)
                try:
                    with rarfile.RarFile(file_path) as rf:
                        rf.extractall(pwd=pwd)
                    print("Found password:" + pwd)
                    return
                except:
                    pass

    def attack_zip(self, file_path, max_count):
        if max_count <= 1:
            print("max_count must greater than 1")
        elif max_count > 16:
            print("max_count must less than 16")

        print("WARRNING: max_count could not be so large, else will time-consuming")

        for i in trange(1, max_count):
            li = self.generate_passwords(i)
            tbar = tqdm(li)
            for pwd in tbar:
                tbar.set_description('Processing ' + pwd)
                try:
                    with ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(pwd=pwd)
                    print("Found password:" + pwd)
                    break
                except Exception as e:
                    pass

    def attack_7z(self, file_path, max_count):
        if max_count <= 1:
            print("max_count must greater than 1")
        elif max_count > 16:
            print("max_count must less than 16")

        print("WARRNING: max_count could not be so large, else will time-consuming")

        for i in trange(1, max_count):
            li = self.generate_passwords(i)
            tbar = tqdm(li)
            for pwd in tbar:
                tbar.set_description('Processing ' + pwd)
                try:
                    with py7zr.SevenZipFile(file_path, mode='r', password=pwd) as z:
                        z.extractall()
                    print("Found password:" + pwd)
                    break
                except Exception as e:
                    pass
