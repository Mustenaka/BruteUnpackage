# Brute Force Unpackage | 暴力破解压缩包密码

一个强大且高效的压缩包密码暴力破解工具。支持 ZIP、RAR 和 7Z 格式，提供字典攻击和暴力破解两种攻击模式。

[English](README.md) | 简体中文

## ✨ 特性

- **支持多种压缩格式**：完整支持 RAR、ZIP 和 7Z 压缩包
- **双重攻击模式**：
  - 基于密码字典的字典攻击
  - 使用自定义字符集的暴力破解攻击
- **多进程支持**：通过使用真正的多进程技术绕过 Python 的 GIL 限制
- **内置字典**：包含来自 SecLists 的综合密码字典
- **灵活配置**：自定义字符集、密码长度和进程数量
- **进度跟踪**：实时显示攻击状态的进度条
- **内存高效**：优化处理大型密码列表和暴力破解范围

## 🎯 工作原理

### 字典攻击
从文本文件加载密码字典，依次尝试每个密码。支持多进程，可以将密码尝试任务分配到多个 CPU 核心。

### 暴力破解攻击
从指定的字符集（大写字母、小写字母、数字、符号）生成所有可能的密码组合，最大长度可自定义。从长度 1 开始递增处理到最大长度。

### 多进程处理
本工具使用 `multiprocessing` 模块创建独立的进程，而不是使用受 Python GIL 限制的线程。每个进程处理一批密码，实现真正的并行执行和最大化 CPU 利用率。

## 📋 系统要求

- Python 3.7+
- 依赖包（见 `requirements.txt`）
- RAR 支持：需要 UnRAR 库

## 🚀 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/Mustenaka/brute_force_unpackage.git
cd brute_force_unpackage
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 安装 UnRAR 库（用于 RAR 支持）

#### macOS
```bash
# 使用 Homebrew 安装
brew install libunrar

# 或者从源码编译
wget https://www.rarlab.com/rar/unrarsrc-6.2.12.tar.gz
tar -xzf unrarsrc-6.2.12.tar.gz
cd unrar
make lib
sudo make install-lib

# 设置环境变量
export UNRAR_LIB_PATH="/usr/local/lib/libunrar.so"
```

#### Linux
```bash
# 从源码编译
wget https://www.rarlab.com/rar/unrarsrc-6.2.12.tar.gz
tar -xzf unrarsrc-6.2.12.tar.gz
cd unrar
make lib
sudo make install-lib

# 设置环境变量（添加到 ~/.bashrc 或 ~/.zshrc）
export UNRAR_LIB_PATH="/usr/local/lib/libunrar.so"
```

#### Windows
```bash
# 从 https://www.rarlab.com/rar_add.htm 下载 UnRAR DLL
# 解压 UnRAR.dll 到系统目录或项目目录
# 设置环境变量
set UNRAR_LIB_PATH=C:\path\to\UnRAR.dll
```

## 📖 使用方法

### 基本语法

```bash
python main.py <archive_file> [选项]
```

### 命令行选项

#### 必需参数
- `file` - 加密压缩包的路径（RAR/ZIP/7Z）

#### 字典攻击选项
- `-d, --dictionary` - 启用字典攻击模式
- `-p, --dict-path PATH` - 密码字典目录路径（默认：password_list）

#### 暴力破解攻击选项
- `-b, --brute` - 启用暴力破解攻击模式
- `-u, --uppercase` - 在暴力破解中包含大写字母（A-Z）
- `-l, --lowercase` - 在暴力破解中包含小写字母（a-z）
- `-n, --digits` - 在暴力破解中包含数字（0-9）
- `-s, --symbols` - 在暴力破解中包含特殊符号
- `-m, --max-length N` - 暴力破解的最大密码长度（默认：8，最大：16）

#### 性能选项
- `-t, --threads N` - 使用的并行进程数（默认：CPU 核心数）
  - 设置为 1 禁用多进程
  - 留空使用所有可用 CPU 核心

### 使用示例

#### 字典攻击（单进程）
```bash
# 使用默认密码列表，单进程
python main.py archive.zip -d -t 1
```

#### 字典攻击（多进程）
```bash
# 使用所有 CPU 核心
python main.py archive.rar -d

# 使用指定数量的进程
python main.py archive.7z -d -t 4

# 使用自定义字典路径
python main.py archive.zip -d -p /path/to/custom/dictionaries -t 8
```

#### 暴力破解攻击
```bash
# 小写字母 + 数字，最大长度 6，多进程
python main.py archive.zip -b -l -n -m 6

# 大写 + 小写 + 数字，最大长度 4，8 进程
python main.py archive.rar -b -u -l -n -m 4 -t 8

# 所有字符集，最大长度 5
python main.py archive.7z -b -u -l -n -s -m 5
```

#### 组合攻击
```bash
# 先尝试字典攻击，如果未找到则进行暴力破解
python main.py archive.rar -d -b -l -n -m 5 -t 4
```

### 脚本运行器（可选）

为方便使用，可以使用提供的脚本：

#### Windows
```bash
# 批处理文件
run.bat

# PowerShell
./run.ps1
```

#### Linux/macOS
```bash
chmod +x run.sh
./run.sh
```

## 🗂️ 项目结构

```
brute_force_unpackage/
├── main.py                          # 主入口点
├── requirements.txt                 # Python 依赖
├── README.md                        # 英文文档
├── README_zh_CN.md                  # 中文文档（本文件）
│
├── src/
│   ├── core/                        # 核心功能
│   │   ├── base_attacker.py        # 攻击的抽象基类
│   │   ├── archive_handlers.py     # 压缩格式处理器（RAR/ZIP/7Z）
│   │   └── multiprocess_attacker.py # 多进程实现
│   │
│   ├── attackers/                   # 攻击实现
│   │   ├── dictionary_attacker.py  # 字典攻击
│   │   └── bruteforce_attacker.py  # 暴力破解攻击
│   │
│   ├── dic_unpack/                  # 旧版字典模块（已弃用）
│   └── rnd_unpack/                  # 旧版随机模块（已弃用）
│
├── password_list/                   # 内置密码字典
│   ├── Common-Credentials/          # 常见密码
│   ├── Default-Credentials/         # 默认设备密码
│   ├── Books/                       # 基于书籍的密码
│   └── ...                          # 更多字典
│
├── origin_file/                     # 用于验证的测试文件
├── rarlib/                          # UnRAR 库二进制文件
└── scripts/
    ├── run.bat                      # Windows 批处理脚本
    ├── run.ps1                      # Windows PowerShell 脚本
    └── run.sh                       # Linux/macOS Shell 脚本
```

## 🔧 架构设计

### 设计模式

1. **策略模式**：不同的压缩格式（RAR、ZIP、7Z）由实现通用接口的独立处理器类处理
2. **模板方法**：基础攻击类提供通用攻击逻辑，字典和暴力破解模式有各自的具体实现
3. **工厂模式**：根据文件扩展名创建相应的压缩包处理器

### 多进程 vs 多线程

本工具使用**多进程**而非多线程来克服 Python 的全局解释器锁（GIL）限制：

- **多线程**：受 GIL 限制，同一时间只有一个线程执行 Python 代码（伪并行）
- **多进程**：创建独立的 Python 进程，每个都有自己的解释器和内存空间（真并行）

每个工作进程：
1. 接收一批要测试的密码
2. 独立尝试解压压缩包
3. 找到密码或处理完所有密码后报告结果

这种方法最大化了 CPU 利用率，在多核系统上显著减少破解时间。

## 📚 内置字典

本项目包含来自 [SecLists](https://github.com/danielmiessler/SecLists) 项目的密码字典：

- 常见密码（top 100、1000、10000 等）
- 默认设备凭据
- 基于年份的密码（1900-2020）
- 书名及变体
- 泄露的密码数据库

## ⚠️ 性能注意事项

### 字典攻击
- 加载大型字典可能需要时间和内存
- 多进程对字典攻击非常有效
- 建议：使用 4-8 个进程以获得最佳平衡

### 暴力破解攻击
- 复杂度随密码长度呈指数增长
- 字符集大小影响组合数：
  - 仅小写字母（26）：26^n 种组合
  - 小写字母 + 数字（36）：36^n 种组合
  - 所有字符集（95）：95^n 种组合
- 建议最大长度：8-10 个字符
- 暴力破解攻击务必使用多进程

### 示例时间估计（大约）
- 4 字符小写+数字：几秒到几分钟
- 6 字符小写+数字：几分钟到几小时
- 8 字符小写+数字：几天到几周
- 8 字符所有字符集：几个月到几年

## 🛡️ 法律免责声明

**本工具仅用于教育和授权安全测试目的。**

- 仅在您拥有或明确授权测试的压缩包上使用
- 未经授权访问计算机系统是非法的
- 作者对本工具的滥用不承担任何责任
- 始终遵守当地法律法规

## 🤝 贡献

欢迎贡献！请随时提交拉取请求或针对以下内容开启问题：
- Bug 修复
- 性能改进
- 新功能
- 文档更新

## 📄 许可证

本项目是开源的。请查看许可证文件了解详情。

## 👤 作者

**Mustenaka**
- GitHub：[@Mustenaka](https://github.com/Mustenaka)
- 博客：[https://www.mustenaka.cn](https://www.mustenaka.cn)

## 📝 更新日志

### 版本 2.0（最新）
- ✨ 使用策略模式完全重构架构
- ✨ 实现真正的多进程支持（绕过 GIL）
- ✨ 添加全面的英文文档和注释
- ✨ 改进命令行参数命名和验证
- ✨ 多进程模式的进度跟踪
- ✨ 更好的错误处理和用户反馈
- 🐛 修复参数命名（simbol→symbols，brust→brute）
- 🗑️ 弃用旧版模块（保留以兼容）

### 版本 1.0（原始版本）
- 基础字典攻击支持
- 基础暴力破解攻击支持
- RAR、ZIP、7Z 格式支持
- 单线程执行

## 🔗 参考资料

- [SecLists 密码字典](https://github.com/danielmiessler/SecLists)
- [UnRAR 库](https://www.rarlab.com/rar_add.htm)
- [Python multiprocessing 文档](https://docs.python.org/3/library/multiprocessing.html)

## 📞 支持

如果遇到问题：
1. 检查所有依赖项是否已安装
2. 验证 UnRAR 库是否正确配置
3. 确保您有权访问压缩包文件
4. 在 GitHub 上提交包含详细错误信息的问题

---

**⭐ 如果您觉得这个工具有用，请考虑在 GitHub 上给它一个星标！**
