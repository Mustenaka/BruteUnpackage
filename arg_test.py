import argparse


def resolving():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='这是一个命令行参数示例程序')

    # 添加位置参数
    parser.add_argument('arg1', help='第一个参数')
    parser.add_argument('arg2', help='第二个参数')

    # 添加可选参数
    parser.add_argument('--optional', help='可选参数', action='store_true')

    # 解析命令行参数
    args = parser.parse_args()

    # 打印命令行参数
    print('arg1:', args.arg1)
    print('arg2:', args.arg2)
    print('optional:', args.optional)


if __name__ == "__main__":
    resolving()
