from unrar import rarfile
from zipfile import ZipFile
from tqdm import tqdm, trange

from src.dic_unpack.Singleton import Singleton

import os
import sys
import time


class DicUnpack(Singleton):
    _data_loaded = False
    _txt_files = []
    dic_path = ""

    def __init__(self, dic_path):
        if not self._data_loaded:
            self.dic_path = dic_path
            self._load_txt_files(dic_path)
            self._data_loaded = True

    def _load_txt_files(self, dic_path):
        for root, dirs, files in os.walk(dic_path):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        # self._txt_files.extend(f.readlines())
                        for line in f:
                            self._txt_files.append(line.strip())

    def rar_attack(self, file_path):
        tbar = tqdm(self._txt_files)
        for line in tbar:
            tbar.set_description('Processing ' + line)
            try:
                file = rarfile.RarFile(file_path, 'r', pwd=line)
                print("Found password:" + line)
                break
            except:
                pass

    def zip_attack(self, file_path):
        tbar = tqdm(self._txt_files)
        for line in tbar:
            tbar.set_description('Processing ' + line)
            try:
                with ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(pwd=line)
                print("Found password:" + line)
                break
            except Exception as e:
                pass
