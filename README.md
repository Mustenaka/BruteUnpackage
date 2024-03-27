# BruteUnpackage | 暴力破解压缩包密码

暴力破解压缩包密码，支持zip, rar 等主流压缩包工具（纯代码版），内置一个常见密码压缩表，密码表用尽后启动随机数便利，最大支持密码位数为127（这也是rar最大长度），自动从小开始向大破解，支持多线程，具体所需要的破解时间根据密码复杂度。

Brute force compression package password, support zip, rar and other mainstream compression package tools (pure code version), built-in a common password compression table, password table exhausted after starting random number convenience, the maximum support password number is 127 (which is also the maximum length of rar), automatically from small to large crack, support multi-threading, The time required to crack the password depends on the password complexity.

### Built-in dictionary |  内置字典

reference: https://github.com/danielmiessler/SecLists/tree/master

### Environment｜环境

```
pip install -r requirements.txt
```

### run ｜ 运行

按照默认的方式直接运行.

Run directly as default

Windows：

```
start run.bat
```

Linux | macOS:

```
./run.sh
```

### Command｜命令

python main.py -t {thread_count} -b {password_book} -p {password_book_dir} ...

-t {thread_count} 使用线程数, 0或1为不使用多线程

-b {password_book} 是否使用字典 True 使用, False 不使用

-p {password_book_dir} 字典的所在位置

### Contribution | 贡献

Mustenaka | https://github.com/Mustenaka