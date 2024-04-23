from src.dic_unpack.dic_unpack import DicUnpack
from src.rnd_unpack.rnd_unpack import RndUnpack
import argparse
import os


def arg_resolving():
    # create ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Brute force cracking the compressed package")

    # add must being param
    parser.add_argument('file', help="unpackage file path", type=str)

    # add optional param
    # use password dictionary
    parser.add_argument(
        '-d', '--dic',
        help="use password dictionary, false is not use, true is use dictionary",
        action='store_true')
    parser.add_argument(
        '-p', '--dicpath',
        help="dictionary path, default is inner dictionary, path should be a folder",
        default="password_list")

    # use random generate
    parser.add_argument(
        '-b', '--brust',
        help="Use generate numeric sequential traversal, false is not use, true is use",
        action='store_true')
    parser.add_argument(
        '-u', '--uppercase',
        help="generated using uppercase letters,",
        action='store_true')
    parser.add_argument(
        '-l', '--lowercase',
        help="generated using lowercase letters",
        action='store_true')
    parser.add_argument(
        '-n', '--number',
        help="generated using numbers",
        action='store_true')
    parser.add_argument(
        '-s', '--simbol',
        help="generated using special simbol",
        action='store_true')
    parser.add_argument(
        '-m', '--max',
        help="generated using special simbol",
        default=8, type=int)

    # thread
    parser.add_argument(
        '-t', '--thread',
        help="thread usage, default is 1",
        action='store_true')

    # 解析命令行参数
    args = parser.parse_args()
    return args


def main(args):
    # 解析命令行参数
    file_path = args.file
    print("unpackage file path:" + file_path)

    # open file
    if not os.path.isfile(file_path):
        print("package file does not exist.")
        return

    _, file_extension = os.path.splitext(file_path)

    # if use password list path.
    if args.dic:
        dicunpack = DicUnpack(dic_path=args.dicpath)
        print("password library path:" + args.dicpath)

        if file_extension == ".rar":
            dicunpack.attack_rar(file_path=file_path)
        elif file_extension == ".zip":
            dicunpack.attack_zip(file_path=file_path)
        elif file_extension == ".7z":
            dicunpack.attack_7z(file_path=file_path)

    # if use generate password
    if args.brust:
        rndunpack = RndUnpack(
            include_lower_letter=args.lowercase,
            include_upper_letter=args.uppercase,
            include_number=args.number,
            include_speical=args.simbol,
        )
        max_length = args.max

        if file_extension == ".rar":
            rndunpack.attack_rar(file_path=file_path, max_count=max_length)
        elif file_extension == ".zip":
            rndunpack.attack_zip(file_path=file_path, max_count=max_length)
        elif file_extension == ".7z":
            rndunpack.attack_7z(file_path=file_path, max_count=max_length)


if __name__ == "__main__":
    args = arg_resolving()
    main(args)
