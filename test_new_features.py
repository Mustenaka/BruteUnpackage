"""
Test script to demonstrate the new architecture and multiprocessing features.

This script shows how to use the refactored codebase programmatically.
"""

import sys
import os

# Try to import handlers, handle missing UnRAR library gracefully
RAR_AVAILABLE = True
try:
    from src.core.archive_handlers import get_handler_for_file, RARHandler, ZIPHandler, SevenZHandler
except (LookupError, ImportError):
    # UnRAR library not configured - import only what's available
    RAR_AVAILABLE = False
    print("[WARNING] UnRAR library not available. RAR tests will be skipped.\n")

    # Import ZIPHandler and SevenZHandler directly (they don't need UnRAR)
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.attackers.dictionary_attacker import DictionaryAttacker
from src.attackers.bruteforce_attacker import BruteforceAttacker
from src.core.multiprocess_attacker import MultiprocessAttacker


def test_archive_handlers():
    """Test the archive handler factory and individual handlers."""
    print("=" * 70)
    print("Testing Archive Handlers")
    print("=" * 70)

    if not RAR_AVAILABLE:
        print("⚠ Skipping archive handler tests (UnRAR library not available)")
        print()
        return

    # Test factory function
    test_files = {
        "test.zip": ZIPHandler,
        "test.rar": RARHandler,
        "test.7z": SevenZHandler
    }

    for filename, expected_class in test_files.items():
        try:
            handler = get_handler_for_file(filename)
            assert isinstance(handler, expected_class)
            print(f"✓ {filename} -> {handler.get_format_name()} handler")
        except Exception as e:
            print(f"✗ {filename} -> Error: {e}")

    # Test unsupported format
    try:
        get_handler_for_file("test.tar.gz")
        print("✗ Should have raised ValueError for unsupported format")
    except ValueError as e:
        print(f"✓ Correctly rejected unsupported format: {e}")

    print()


def test_dictionary_attacker():
    """Test the dictionary attacker initialization and password loading."""
    print("=" * 70)
    print("Testing Dictionary Attacker")
    print("=" * 70)

    try:
        # Test with default path
        attacker = DictionaryAttacker()
        print(f"✓ Dictionary attacker created")
        print(f"  Loaded {len(attacker.passwords)} passwords")

        # Show sample passwords
        if attacker.passwords:
            print(f"  Sample passwords: {attacker.passwords[:5]}")

    except Exception as e:
        print(f"✗ Error: {e}")

    print()


def test_bruteforce_attacker():
    """Test the brute-force attacker initialization and password generation."""
    print("=" * 70)
    print("Testing Brute-force Attacker")
    print("=" * 70)

    try:
        # Test with small parameters
        attacker = BruteforceAttacker(
            include_lowercase=True,
            include_digits=True,
            include_uppercase=False,
            include_symbols=False,
            max_length=3
        )
        print(f"✓ Brute-force attacker created")
        print(f"  Character set: {attacker.charset}")

        # Generate passwords of length 2
        passwords = attacker.generate_passwords_of_length(2)
        print(f"  Generated {len(passwords)} passwords of length 2")
        print(f"  Sample: {passwords[:10]}")

    except Exception as e:
        print(f"✗ Error: {e}")

    print()


def test_multiprocess_attacker():
    """Test the multiprocessing attacker initialization."""
    print("=" * 70)
    print("Testing Multiprocess Attacker")
    print("=" * 70)

    try:
        # Test with default settings
        mp_attacker = MultiprocessAttacker()
        print(f"✓ Multiprocess attacker created")
        print(f"  Number of processes: {mp_attacker.num_processes}")

        # Test password splitting
        test_passwords = [f"pass{i}" for i in range(100)]
        chunks = mp_attacker.split_passwords(test_passwords)
        print(f"  Split 100 passwords into {len(chunks)} chunks")
        print(f"  Chunk sizes: {[len(chunk) for chunk in chunks]}")

    except Exception as e:
        print(f"✗ Error: {e}")

    print()


def test_parameter_validation():
    """Test parameter validation in various components."""
    print("=" * 70)
    print("Testing Parameter Validation")
    print("=" * 70)

    # Test invalid character set (none selected)
    try:
        BruteforceAttacker(
            include_uppercase=False,
            include_lowercase=False,
            include_digits=False,
            include_symbols=False
        )
        print("✗ Should have raised ValueError for empty character set")
    except ValueError as e:
        print(f"✓ Correctly rejected empty character set: {e}")

    # Test invalid dictionary path
    try:
        DictionaryAttacker(dictionary_path="/nonexistent/path")
        print("✗ Should have raised FileNotFoundError")
    except FileNotFoundError as e:
        print(f"✓ Correctly rejected invalid path: {e}")

    # Test invalid max length
    try:
        BruteforceAttacker(max_length=0)
        print("✗ Should have raised ValueError for max_length=0")
    except ValueError as e:
        print(f"✓ Correctly rejected invalid max_length: {e}")

    print()


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "Brute Force Unpackage - Feature Tests" + " " * 16 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")

    test_archive_handlers()
    test_dictionary_attacker()
    test_bruteforce_attacker()
    test_multiprocess_attacker()
    test_parameter_validation()

    print("=" * 70)
    print("All tests completed!")
    print("=" * 70)
    print("\nNote: These are basic functionality tests.")
    print("To test actual password cracking, use the main.py script with a real archive file.")
    print("\nExample:")
    print("  python main.py origin_file/test.zip -d -t 4")
    print()


if __name__ == "__main__":
    main()
