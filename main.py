import os
os.environ.setdefault(
        "UNRAR_LIB_PATH", "/Users/andrew/Projects/PythonProjects/Tools/brute_force_unpackage/rarlib/libunrar.so")

from src.dic_unpack.dic_unpack import DicUnpack


def main(file_name):
    # open file
    if not os.path.isfile(file_name):
        print("file does not exist.")

    # use Dictionary Unpack
    dic_unpack = DicUnpack("password_list")
    if file_name.endswith('.rar'):
        dic_unpack.rar_attack(file_name)
    elif file_name.endswith('.zip'):
        dic_unpack.zip_attack(file_name)


if __name__ == "__main__":

    # file_name = sys.argv[1]
    # main(file_name=file_name)
    main(file_name="origin_file/test.rar")
