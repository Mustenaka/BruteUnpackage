# BruteUnpackage | 暴力破解压缩包密码

暴力破解压缩包密码，支持zip, rar 等主流压缩包工具（纯代码版），内置一个常见密码压缩表，密码表用尽后启动随机数便利，最大支持密码位数为16，自动从小开始向大破解，支持多线程，具体所需要的破解时间根据密码复杂度。

Brute force compression package password, support zip, rar and other mainstream compression package tools (pure code version), built-in a common password compression table, password table exhausted after starting random number convenience, the maximum support password length is 16, automatically from small to large crack, support multi-threading, The time required to crack the password depends on the password complexity. eWEEIt provides flexibility in password cracking methods and supports various types of compressed packages such as RAR, ZIP, and 7z.

### Built-in dictionary |  内置字典

reference: https://github.com/danielmiessler/SecLists/tree/master

### Environment｜环境

#### Clone the repository ｜ 克隆、下载本项目
```
git clone https://github.com/username/repository.git
```

#### Install dependencies ｜ 安装Python相关依赖环境

```
pip install -r requirements.txt
```

#### RAR environment ｜ RAR环境

需要在RAR安装环境中配置UNRAR_LIB_PATH，MacOS、Linux需要自主编译.so文件，Windows需要配置.dll环境

Set the environment variable UNRAR_LIB_PATH to the path of the libunrar.so library. For example:

```
export UNRAR_LIB_PATH="/path/to/libunrar.so"
```

### run ｜ 运行

#### Python直接运行

```
python brute_force_unpack.py [-h] [-d] [-p DICPATH] [-b] [-u] [-l] [-n] [-s] [-m MAX] [-t] file
```

- `file`: Path to the compressed package file.

##### Optional Arguments ｜ 可选参数（懒得写中文了，自己看）

- `-h, --help`: Show the help message and exit.
- `-d, --dic`: Use a password dictionary. (Default: false)
- `-p DICPATH, --dicpath DICPATH`: Specify the path to the password dictionary. (Default: "password_list")
- `-b, --brust`: Use random password generation. (Default: false)
- `-u, --uppercase`: Include uppercase letters in generated passwords.
- `-l, --lowercase`: Include lowercase letters in generated passwords.
- `-n, --number`: Include numbers in generated passwords.
- `-s, --simbol`: Include special symbols in generated passwords.
- `-m MAX, --max MAX`: Specify the maximum length of generated passwords. (Default: 8)
- `-t, --thread`: Enable multi-threading for faster processing. (Default: false)

### script run

在对应的操作系统使用脚本运行

#### Windows：

```
start run.bat
```

#### Linux | macOS:

```
./run.sh
```

## project struct | 文件结构

- password_list: 密码本存储器
- rarlib: unrar so|dll文件，目前只有m1 macOS平台编译版本，待更新，需要补充和script脚本组合
- src: 源代码
- main.py 主运行代码

## Contribution | 贡献

Mustenaka | https://github.com/Mustenaka