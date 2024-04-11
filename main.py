import argparse
import os
os.environ.setdefault(
    "UNRAR_LIB_PATH", "/Users/andrew/Projects/PythonProjects/Tools/brute_force_unpackage/rarlib/libunrar.so")
from src.dic_unpack.dic_unpack import DicUnpack

def arg_resolving():
    # create ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Brute force cracking the compressed package")

    # add must being param
    parser.add_argument('-f', '--file', help="unpackage file")

    # add optional param
    parser.add_argument(
        '-d', '--dic',
        help="use password dictionary, false is not use, true is use dictionary",
        action='store_true')
    parser.add_argument(
        '-p', '--path',
        help="dictionary path, default is inner dictionary, path should be a folder",
        action='store_true')

    parser.add_argument(
        '-b', '--brust',
        help="Use generate numeric sequential traversal, false is not use, true is use",
        action='store_true')
    parser.add_argument(
        '-u', '--uppercase',
        help="generated using uppercase letters,", action='store_true')
    parser.add_argument(
        '-l', '--lowercase',
        help="generated using lowercase letters", action='store_true')
    parser.add_argument(
        '-n', '--number',
        help="generated using numbers", action='store_true')
    parser.add_argument(
        '-s', '--simbol',
        help="generated using special simbol", action='store_true')

    parser.add_argument(
        '-t', '--thread',
        help="thread usage, default is 1", action='store_true')

    # 解析命令行参数
    args = parser.parse_args()
    return args


def main(args):
    # 解析命令行参数
    file_name = args.file
    print("unpackage file path" + file_name)

    # open file
    if not os.path.isfile(file_name):
        print("package file does not exist.")
        return

    # use Dictionary Unpack
    # dic_unpack = DicUnpack("password_list")
    # if file_name.endswith('.rar'):
    #     dic_unpack.rar_attack(file_name)
    # elif file_name.endswith('.zip'):
    #     dic_unpack.zip_attack(file_name)


if __name__ == "__main__":
    args = arg_resolving()
    main(args)
