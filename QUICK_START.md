# Quick Start Guide | 快速开始指南

## English

### Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) For RAR support, install UnRAR library
# macOS:
brew install libunrar
export UNRAR_LIB_PATH="/usr/local/lib/libunrar.so"
```

### Basic Usage
```bash
# Dictionary attack
python main.py archive.zip -d

# Brute-force attack (lowercase + digits, max length 4)
python main.py archive.rar -b -l -n -m 4

# Use multiprocessing (4 processes)
python main.py archive.7z -d -t 4

# Combined attack
python main.py archive.zip -d -b -l -n -m 5 -t 4
```

### Get Help
```bash
python main.py -h
```

---

## 中文

### 安装
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. (可选) RAR支持需要安装UnRAR库
# macOS:
brew install libunrar
export UNRAR_LIB_PATH="/usr/local/lib/libunrar.so"
```

### 基本用法
```bash
# 字典攻击
python main.py archive.zip -d

# 暴力破解（小写+数字，最大长度4）
python main.py archive.rar -b -l -n -m 4

# 使用多进程（4个进程）
python main.py archive.7z -d -t 4

# 组合攻击
python main.py archive.zip -d -b -l -n -m 5 -t 4
```

### 获取帮助
```bash
python main.py -h
```

---

## Key Features | 主要特性

✅ **Multiple Formats** | 多格式支持: RAR, ZIP, 7Z
✅ **Dictionary Attack** | 字典攻击: Use password lists
✅ **Brute-force** | 暴力破解: Generate all combinations
✅ **Multiprocessing** | 多进程: 4-8x faster on multi-core CPUs
✅ **Progress Tracking** | 进度跟踪: Real-time progress bars

## Documentation | 文档

- **README.md** - Complete documentation (English)
- **改进说明.md** - Improvement guide (Chinese)
- **ARCHITECTURE.md** - Architecture details
- **USAGE_EXAMPLES.md** - Detailed usage examples
- **IMPROVEMENTS_SUMMARY.md** - Complete improvement summary

## Version | 版本

**Current: v2.0** - Complete professional upgrade
- Refactored architecture
- Multiprocessing support
- 7x performance improvement
- Comprehensive documentation
