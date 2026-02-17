# Architecture Documentation

## Overview

This document describes the architecture of the Brute Force Unpackage tool after the Version 2.0 refactoring. The new architecture emphasizes modularity, extensibility, and performance through design patterns and multiprocessing.

## Design Principles

1. **Separation of Concerns**: Different responsibilities are isolated into dedicated modules
2. **Strategy Pattern**: Archive formats are handled by interchangeable handler classes
3. **Template Method**: Common attack logic is defined in base classes
4. **Factory Pattern**: Handlers are created based on file type
5. **DRY (Don't Repeat Yourself)**: Eliminated code duplication through inheritance and composition

## Project Structure

```
src/
├── core/                           # Core framework components
│   ├── base_attacker.py           # Abstract base class for all attacks
│   ├── archive_handlers.py        # Archive format handlers (Strategy pattern)
│   └── multiprocess_attacker.py   # Multiprocessing implementation
│
├── attackers/                      # Attack mode implementations
│   ├── dictionary_attacker.py     # Dictionary-based attacks
│   └── bruteforce_attacker.py     # Brute-force attacks
│
├── dic_unpack/                     # Legacy code (deprecated)
└── rnd_unpack/                     # Legacy code (deprecated)
```

## Core Components

### 1. Base Attacker (`base_attacker.py`)

**Purpose**: Provides the abstract base class and common functionality for all attack modes.

**Key Features**:
- Abstract `generate_passwords()` method for subclasses to implement
- Common `attack()` method with progress tracking
- Consistent interface for all attack types

**Design Pattern**: Template Method Pattern

```python
class BaseAttacker(ABC):
    @abstractmethod
    def generate_passwords(self) -> List[str]:
        """Subclasses must implement password generation"""
        pass

    def attack(self, file_path, archive_handler, password_candidates):
        """Common attack logic with progress tracking"""
        # Attempts each password with progress bar
        # Returns found password or None
```

### 2. Archive Handlers (`archive_handlers.py`)

**Purpose**: Encapsulate archive format-specific extraction logic.

**Key Features**:
- Abstract `ArchiveHandler` base class
- Concrete implementations: `RARHandler`, `ZIPHandler`, `SevenZHandler`
- Factory function `get_handler_for_file()` for automatic handler selection
- Consistent `try_extract()` interface

**Design Pattern**: Strategy Pattern + Factory Pattern

```python
class ArchiveHandler(ABC):
    @abstractmethod
    def try_extract(self, file_path: str, password: str) -> bool:
        """Attempt extraction with given password"""
        pass

def get_handler_for_file(file_path: str) -> ArchiveHandler:
    """Factory function to create appropriate handler"""
    # Returns RARHandler, ZIPHandler, or SevenZHandler based on extension
```

**Benefits**:
- Easy to add new archive formats
- Eliminates duplicate code across attack modes
- Testable in isolation

### 3. Multiprocess Attacker (`multiprocess_attacker.py`)

**Purpose**: Implements true parallelism to bypass Python's GIL.

**Key Features**:
- Automatic password distribution across processes
- Inter-process communication via `multiprocessing.Queue`
- Progress tracking across all workers
- Graceful termination when password is found

**Architecture**:

```
Main Process
    ├── Split passwords into N chunks (N = CPU cores)
    ├── Create N worker processes
    ├── Monitor results via Queue
    └── Terminate all workers when password found

Worker Process 1
    └── Test passwords from chunk 1

Worker Process 2
    └── Test passwords from chunk 2

...

Worker Process N
    └── Test passwords from chunk N
```

**Why Multiprocessing vs Threading?**

Python's Global Interpreter Lock (GIL) prevents multiple threads from executing Python code simultaneously. This makes threading ineffective for CPU-intensive tasks like password cracking.

Multiprocessing creates separate Python interpreter processes, each with its own GIL, enabling true parallel execution on multiple CPU cores.

**Performance Impact**:
- 1 process: 100% utilization of 1 core
- 4 processes: ~400% total CPU utilization (4 cores)
- 8 processes: ~800% total CPU utilization (8 cores)

### 4. Dictionary Attacker (`dictionary_attacker.py`)

**Purpose**: Implements dictionary-based password attacks.

**Key Features**:
- Loads passwords from text files recursively
- Deduplicates passwords using sets
- Supports both single-process and multiprocess modes
- Memory-efficient loading with error handling

**Process Flow**:
```
Initialize
    └── Load dictionaries from path
        ├── Walk directory tree
        ├── Read all .txt files
        ├── Deduplicate passwords
        └── Store in memory

Attack
    ├── Get archive handler
    ├── Choose single-process or multiprocess
    └── Attempt all passwords
        └── Return found password or None
```

### 5. Brute-force Attacker (`bruteforce_attacker.py`)

**Purpose**: Implements brute-force attacks with configurable character sets.

**Key Features**:
- Customizable character sets (uppercase, lowercase, digits, symbols)
- Incremental length testing (1 to max_length)
- Efficient password generation using `itertools.product`
- Warning system for large search spaces

**Process Flow**:
```
Initialize
    ├── Build character set from options
    ├── Calculate total combinations
    └── Display warnings if needed

Attack
    └── For each length from 1 to max_length:
        ├── Generate all passwords of that length
        ├── Attempt passwords (single or multiprocess)
        └── Return if password found
```

**Complexity Analysis**:

For character set size `C` and max length `L`:
- Total combinations: `C^1 + C^2 + ... + C^L`
- Examples:
  - lowercase (26 chars), length 6: ~309 million combinations
  - lowercase + digits (36 chars), length 6: ~2.2 billion combinations
  - all chars (95 chars), length 6: ~735 billion combinations

## Data Flow

### Dictionary Attack Flow

```
User Input (main.py)
    ↓
Parse Arguments
    ↓
Validate File
    ↓
Get Archive Handler (factory)
    ↓
Create Dictionary Attacker
    ↓
Load Dictionaries
    ↓
Choose Mode:
    ├── Single Process → BaseAttacker.attack()
    └── Multiprocess → MultiprocessAttacker.attack()
            ├── Split passwords
            ├── Create workers
            ├── Distribute work
            └── Collect results
                ↓
            Found Password?
                ├── Yes → Display success
                └── No → Display failure
```

### Brute-force Attack Flow

```
User Input (main.py)
    ↓
Parse Arguments
    ↓
Validate File
    ↓
Get Archive Handler (factory)
    ↓
Create Brute-force Attacker
    ├── Build character set
    └── Calculate combinations
        ↓
For length = 1 to max_length:
    ├── Generate passwords
    ├── Choose Mode:
    │   ├── Single Process → BaseAttacker.attack()
    │   └── Multiprocess → MultiprocessAttacker.attack()
    └── Password found?
        ├── Yes → Return and exit
        └── No → Continue to next length
```

## Key Improvements from Version 1.0

### 1. Eliminated Code Duplication

**Before (v1.0)**:
- `attack_rar()`, `attack_zip()`, `attack_7z()` repeated in both `DicUnpack` and `RndUnpack`
- 6 nearly-identical methods with only handler differences

**After (v2.0)**:
- Single `attack()` method in `BaseAttacker`
- Archive-specific logic in handler classes
- ~70% code reduction

### 2. Implemented True Multiprocessing

**Before (v1.0)**:
- Thread module existed but was empty
- No parallel execution capability
- Single-threaded only

**After (v2.0)**:
- Full multiprocessing implementation
- Automatic CPU core detection
- Configurable process count
- ~4-8x performance improvement on multi-core systems

### 3. Improved Architecture

**Before (v1.0)**:
- Monolithic classes with mixed responsibilities
- Tight coupling between attack modes and formats
- Singleton pattern misuse

**After (v2.0)**:
- Clean separation of concerns
- Strategy pattern for extensibility
- Loosely coupled components
- Easy to test and maintain

### 4. Better Error Handling

**Before (v1.0)**:
- Generic exception catching
- Silent failures
- No validation

**After (v2.0)**:
- Specific exception types
- Input validation
- Informative error messages
- Graceful degradation

### 5. Enhanced User Experience

**Before (v1.0)**:
- Minimal feedback
- Typos in parameters (`simbol`, `brust`)
- No usage examples

**After (v2.0)**:
- Detailed progress tracking
- Fixed parameter names
- Comprehensive help text
- Usage examples in README

## Extension Points

### Adding New Archive Format

1. Create new handler class in `archive_handlers.py`:
```python
class NewFormatHandler(ArchiveHandler):
    def try_extract(self, file_path: str, password: str) -> bool:
        # Implement extraction logic
        pass

    def get_format_name(self) -> str:
        return "NEW_FORMAT"
```

2. Register in factory function:
```python
def get_handler_for_file(file_path: str) -> ArchiveHandler:
    handlers = {
        '.rar': RARHandler(),
        '.zip': ZIPHandler(),
        '.7z': SevenZHandler(),
        '.new': NewFormatHandler(),  # Add new handler
    }
    # ...
```

### Adding New Attack Mode

1. Create new attacker class inheriting from `BaseAttacker`:
```python
class NewAttacker(BaseAttacker):
    def generate_passwords(self) -> List[str]:
        # Implement password generation logic
        pass

    def attack_file(self, file_path, archive_handler, ...):
        # Implement attack logic
        pass
```

2. Integrate in `main.py`:
```python
if args.new_mode:
    attacker = NewAttacker(...)
    found_password = attacker.attack_file(...)
```

## Performance Optimization Strategies

### 1. Password Distribution

The multiprocessing implementation distributes passwords evenly across workers:
```python
chunk_size = ceil(total_passwords / num_processes)
```

This ensures balanced workload and maximum CPU utilization.

### 2. Early Termination

When any worker finds the password:
```python
queue.put(('found', password, worker_id))
# Main process terminates all workers immediately
for p in processes:
    if p.is_alive():
        p.terminate()
```

This prevents wasted computation.

### 3. Memory Efficiency

- Dictionary attacker loads all passwords once (shared read-only data)
- Brute-force attacker generates passwords incrementally by length
- Temporary directory usage prevents disk clutter

### 4. Progress Tracking

Uses `tqdm` for real-time feedback without performance overhead:
```python
tbar = tqdm(passwords, desc="Attempting passwords")
for password in tbar:
    tbar.set_description(f'Trying: {password}')
```

## Security Considerations

### What This Tool Does

- Tests password strength of YOUR archives
- Educational demonstration of brute-force attacks
- Security research and testing

### What This Tool Should NOT Be Used For

- Unauthorized access to others' files
- Illegal activities
- Bypassing security without permission

### Built-in Safety Features

- Requires explicit file path (no auto-discovery)
- No stealth mode or evasion techniques
- Comprehensive logging of all attempts
- Educational focus in documentation

## Testing Strategy

### Unit Tests (Suggested)

```python
# Test archive handlers
def test_zip_handler():
    handler = ZIPHandler()
    assert handler.get_format_name() == "ZIP"

# Test password generation
def test_bruteforce_generator():
    attacker = BruteforceAttacker(include_lowercase=True, max_length=2)
    passwords = attacker.generate_passwords_of_length(2)
    assert len(passwords) == 26 * 26

# Test multiprocessing
def test_password_splitting():
    mp = MultiprocessAttacker(num_processes=4)
    chunks = mp.split_passwords(list(range(100)))
    assert len(chunks) == 4
    assert all(len(chunk) == 25 for chunk in chunks)
```

### Integration Tests

Use `test_new_features.py` to verify:
- Handler creation
- Dictionary loading
- Password generation
- Multiprocessing initialization

### Manual Testing

Use test archives in `origin_file/` with known passwords.

## Troubleshooting

### Common Issues

1. **UnRAR library not found**
   - Solution: Install libunrar and set UNRAR_LIB_PATH

2. **Out of memory**
   - Solution: Reduce process count or max-length

3. **Very slow performance**
   - Solution: Reduce character set or max-length

4. **Process hangs**
   - Solution: Use Ctrl+C to interrupt gracefully

## Future Enhancements

Potential improvements for future versions:

1. **GPU Acceleration**: Use CUDA/OpenCL for massive parallelism
2. **Distributed Computing**: Spread work across multiple machines
3. **Smart Dictionary**: Learn from successful passwords
4. **Resume Capability**: Save progress and resume later
5. **Hybrid Attacks**: Combine dictionary with mutations/rules
6. **Cloud Integration**: Use cloud computing for large searches
7. **GUI Interface**: Desktop application with visual progress
8. **Password Analytics**: Statistics on common patterns

## Conclusion

The Version 2.0 architecture provides a solid foundation for password cracking with:

✓ Clean, maintainable code structure
✓ True parallel processing capability
✓ Extensible design for new formats/modes
✓ Comprehensive documentation
✓ Professional error handling
✓ Optimized performance

The refactoring transformed a basic script into a robust, production-ready tool while maintaining simplicity and usability.
