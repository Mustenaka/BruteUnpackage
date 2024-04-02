from unrar import rarfile
from zipfile import ZipFile
from tqdm import tqdm, trange
import py7zr

import os
import sys
import time


class RndUnpack():
    upper_limit = 8
    lib_speical = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    lib_number = "1234567890"
    lib_upper_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lib_lower_letter = "abcdefghijklmnopqrstuvwxyz"
    lib_runtime = []
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
            self.lib_runtime.append(self.lib_upper_letter)

        if include_lower_letter:
            self.lib_runtime.append(self.lib_lower_letter)

        if include_number:
            self.lib_runtime.append(self.lib_number)

        if include_speical:
            self.lib_runtime.append(self.lib_speical)

        print("rnd init, Lib:" + self.lib_runtime)

    def attack_rar(self, file_path, max_count):
        pass

    def attack_zip(self, file_path, max_count):
        pass

    def attack_7z(self, file_path, max_count):
        pass
