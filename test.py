import itertools

def generate_passwords(a, n) -> list:
    # 使用itertools.product生成所有可能的排列组合
    passwords = [''.join(combination) for combination in itertools.product(a, repeat=n)]
    return passwords

# 示例用法
a = "abc"  # 替换为你的字符串
n = 3      # 替换为你想要的密码长度
password_list = generate_passwords(a, n)
print(password_list)