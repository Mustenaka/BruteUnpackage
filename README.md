# Brute Force Unpackage | 暴力破解压缩包密码

A powerful and efficient tool for brute-force password cracking of compressed archives. Supports ZIP, RAR, and 7Z formats with both dictionary-based and brute-force attack modes.

English | [简体中文](README_zh_CN.md)

## ✨ Features

- **Multiple Archive Formats**: Full support for RAR, ZIP, and 7Z archives
- **Dual Attack Modes**:
  - Dictionary-based attacks using password lists
  - Brute-force attacks with customizable character sets
- **Multiprocessing Support**: Bypass Python's GIL limitation by using true multiprocessing
- **Built-in Dictionaries**: Includes comprehensive password dictionaries from SecLists
- **Flexible Configuration**: Customize character sets, password length, and process count
- **Progress Tracking**: Real-time progress bars showing attack status
- **Memory Efficient**: Optimized to handle large password lists and brute-force ranges

## 🎯 How It Works

### Dictionary Attack
Loads password dictionaries from text files and attempts each password sequentially. Supports multiprocessing to distribute password attempts across multiple CPU cores.

### Brute-force Attack
Generates all possible password combinations from specified character sets (uppercase, lowercase, digits, symbols) up to a maximum length. Processes incrementally from length 1 to max length.

### Multiprocessing
Instead of using threading (limited by Python's GIL), this tool uses the `multiprocessing` module to create separate processes. Each process handles a chunk of passwords, enabling true parallel execution and maximum CPU utilization.

## 📋 Requirements

- Python 3.7+
- Required packages (see `requirements.txt`)
- For RAR support: UnRAR library

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Mustenaka/brute_force_unpackage.git
cd brute_force_unpackage
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install UnRAR Library (for RAR support)

#### macOS
```bash
# Install using Homebrew
brew install libunrar

# Or compile from source
wget https://www.rarlab.com/rar/unrarsrc-6.2.12.tar.gz
tar -xzf unrarsrc-6.2.12.tar.gz
cd unrar
make lib
sudo make install-lib

# Set environment variable
export UNRAR_LIB_PATH="/usr/local/lib/libunrar.so"
```

#### Linux
```bash
# Compile from source
wget https://www.rarlab.com/rar/unrarsrc-6.2.12.tar.gz
tar -xzf unrarsrc-6.2.12.tar.gz
cd unrar
make lib
sudo make install-lib

# Set environment variable (add to ~/.bashrc or ~/.zshrc)
export UNRAR_LIB_PATH="/usr/local/lib/libunrar.so"
```

#### Windows
```bash
# Download UnRAR DLL from https://www.rarlab.com/rar_add.htm
# Extract UnRAR.dll to your system or project directory
# Set environment variable
set UNRAR_LIB_PATH=C:\path\to\UnRAR.dll
```

## 📖 Usage

### Basic Syntax

```bash
python main.py <archive_file> [options]
```

### Command-line Options

#### Required Arguments
- `file` - Path to the encrypted archive file (RAR/ZIP/7Z)

#### Dictionary Attack Options
- `-d, --dictionary` - Enable dictionary-based attack mode
- `-p, --dict-path PATH` - Path to password dictionary directory (default: password_list)

#### Brute-force Attack Options
- `-b, --brute` - Enable brute-force attack mode
- `-u, --uppercase` - Include uppercase letters (A-Z) in brute-force
- `-l, --lowercase` - Include lowercase letters (a-z) in brute-force
- `-n, --digits` - Include digits (0-9) in brute-force
- `-s, --symbols` - Include special symbols in brute-force
- `-m, --max-length N` - Maximum password length for brute-force (default: 8, max: 16)

#### Performance Options
- `-t, --threads N` - Number of parallel processes to use (default: CPU count)
  - Set to 1 to disable multiprocessing
  - Leave empty to use all available CPU cores

### Examples

#### Dictionary Attack (Single Process)
```bash
# Use default password lists with single process
python main.py archive.zip -d -t 1
```

#### Dictionary Attack (Multiprocessing)
```bash
# Use all CPU cores
python main.py archive.rar -d

# Use specific number of processes
python main.py archive.7z -d -t 4

# Use custom dictionary path
python main.py archive.zip -d -p /path/to/custom/dictionaries -t 8
```

#### Brute-force Attack
```bash
# Lowercase + digits, max length 6, multiprocessing
python main.py archive.zip -b -l -n -m 6

# Uppercase + lowercase + digits, max length 4, 8 processes
python main.py archive.rar -b -u -l -n -m 4 -t 8

# All character sets, max length 5
python main.py archive.7z -b -u -l -n -s -m 5
```

#### Combined Attack
```bash
# Try dictionary first, then brute-force if not found
python main.py archive.rar -d -b -l -n -m 5 -t 4
```

### Script Runners (Alternative)

For convenience, you can use the provided scripts:

#### Windows
```bash
# Batch file
run.bat

# PowerShell
./run.ps1
```

#### Linux/macOS
```bash
chmod +x run.sh
./run.sh
```

## 🗂️ Project Structure

```
brute_force_unpackage/
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── src/
│   ├── core/                        # Core functionality
│   │   ├── base_attacker.py        # Abstract base class for attacks
│   │   ├── archive_handlers.py     # Archive format handlers (RAR/ZIP/7Z)
│   │   └── multiprocess_attacker.py # Multiprocessing implementation
│   │
│   ├── attackers/                   # Attack implementations
│   │   ├── dictionary_attacker.py  # Dictionary-based attack
│   │   └── bruteforce_attacker.py  # Brute-force attack
│   │
│   ├── dic_unpack/                  # Legacy dictionary module (deprecated)
│   └── rnd_unpack/                  # Legacy random module (deprecated)
│
├── password_list/                   # Built-in password dictionaries
│   ├── Common-Credentials/          # Common passwords
│   ├── Default-Credentials/         # Default device passwords
│   ├── Books/                       # Book-based passwords
│   └── ...                          # More dictionaries
│
├── origin_file/                     # Test files for verification
├── rarlib/                          # UnRAR library binaries
└── scripts/
    ├── run.bat                      # Windows batch script
    ├── run.ps1                      # Windows PowerShell script
    └── run.sh                       # Linux/macOS shell script
```

## 🔧 Architecture

### Design Patterns

1. **Strategy Pattern**: Different archive formats (RAR, ZIP, 7Z) are handled by separate handler classes implementing a common interface
2. **Template Method**: Base attacker class provides common attack logic, with specific implementations for dictionary and brute-force modes
3. **Factory Pattern**: Archive handlers are created based on file extension

### Multiprocessing vs Threading

This tool uses **multiprocessing** instead of threading to overcome Python's Global Interpreter Lock (GIL):

- **Threading**: Limited by GIL, only one thread executes Python code at a time (pseudo-parallelism)
- **Multiprocessing**: Creates separate Python processes, each with its own interpreter and memory space (true parallelism)

Each worker process:
1. Receives a chunk of passwords to test
2. Independently attempts to extract the archive
3. Reports back when password is found or chunk is exhausted

This approach maximizes CPU utilization and significantly reduces cracking time on multi-core systems.

## 📚 Built-in Dictionaries

This project includes password dictionaries from the [SecLists](https://github.com/danielmiessler/SecLists) project:

- Common passwords (top 100, 1000, 10000, etc.)
- Default device credentials
- Year-based passwords (1900-2020)
- Book titles and variations
- Leaked password databases

## ⚠️ Performance Considerations

### Dictionary Attacks
- Loading large dictionaries may take time and memory
- Multiprocessing is highly effective for dictionary attacks
- Recommended: Use 4-8 processes for optimal balance

### Brute-force Attacks
- Complexity grows exponentially with password length
- Character set size impacts combinations:
  - Lowercase only (26): 26^n combinations
  - Lowercase + digits (36): 36^n combinations
  - All sets (95): 95^n combinations
- Recommended maximum length: 8-10 characters
- Always use multiprocessing for brute-force attacks

### Example Timings (approximate)
- 4-char lowercase+digits: seconds to minutes
- 6-char lowercase+digits: minutes to hours
- 8-char lowercase+digits: days to weeks
- 8-char all sets: months to years

## 🛡️ Legal Disclaimer

**This tool is for educational and authorized security testing purposes only.**

- Only use on archives you own or have explicit permission to test
- Unauthorized access to computer systems is illegal
- The authors assume no liability for misuse of this tool
- Always comply with local laws and regulations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- Performance improvements
- New features
- Documentation updates

## 📄 License

This project is open source. Please check the license file for details.

## 👤 Author

**Mustenaka**
- GitHub: [@Mustenaka](https://github.com/Mustenaka)
- Blog: [https://www.mustenaka.cn](https://www.mustenaka.cn)

## 📝 Changelog

### Version 2.0 (Latest)
- ✨ Complete architecture refactoring with strategy pattern
- ✨ Implemented true multiprocessing support (bypasses GIL)
- ✨ Added comprehensive English documentation and comments
- ✨ Improved command-line argument naming and validation
- ✨ Progress tracking for multiprocessing mode
- ✨ Better error handling and user feedback
- 🐛 Fixed parameter naming (simbol→symbols, brust→brute)
- 🗑️ Deprecated legacy modules (kept for compatibility)

### Version 1.0 (Original)
- Basic dictionary attack support
- Basic brute-force attack support
- RAR, ZIP, 7Z format support
- Single-threaded execution

## 🔗 References

- [SecLists Password Dictionaries](https://github.com/danielmiessler/SecLists)
- [UnRAR Library](https://www.rarlab.com/rar_add.htm)
- [Python multiprocessing Documentation](https://docs.python.org/3/library/multiprocessing.html)

## 📞 Support

If you encounter issues:
1. Check that all dependencies are installed
2. Verify UnRAR library is properly configured
3. Ensure you have permission to access the archive file
4. Open an issue on GitHub with detailed error information

---

**⭐ If you find this tool useful, please consider giving it a star on GitHub!**
