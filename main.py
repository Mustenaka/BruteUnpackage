"""
Brute Force Unpackage - Main Entry Point

This is the main entry point for the brute-force archive password cracking tool.
Supports RAR, ZIP, and 7Z formats with both dictionary and brute-force attack modes.
"""

import argparse
import os
import sys

from src.core.archive_handlers import get_handler_for_file
from src.attackers.dictionary_attacker import DictionaryAttacker
from src.attackers.bruteforce_attacker import BruteforceAttacker


def parse_arguments():
    """
    Parse and validate command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Brute-force password cracking tool for compressed archives (RAR/ZIP/7Z)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dictionary attack using default password lists
  python main.py archive.zip -d

  # Dictionary attack with custom dictionary path
  python main.py archive.rar -d -p /path/to/dictionaries

  # Brute-force attack with lowercase + digits, max length 6
  python main.py archive.7z -b -l -n -m 6

  # Use multiprocessing with 4 processes
  python main.py archive.zip -d -t 4

  # Combined: uppercase, lowercase, digits, symbols, max length 4
  python main.py archive.rar -b -u -l -n -s -m 4 -t 8
        """
    )

    # Required argument
    parser.add_argument(
        'file',
        help="Path to the encrypted archive file (RAR/ZIP/7Z)",
        type=str
    )

    # Dictionary attack options
    dict_group = parser.add_argument_group('Dictionary Attack Options')
    dict_group.add_argument(
        '-d', '--dictionary',
        help="Enable dictionary-based attack mode",
        action='store_true'
    )
    dict_group.add_argument(
        '-p', '--dict-path',
        help="Path to password dictionary directory (default: password_list)",
        default="password_list",
        metavar='PATH'
    )

    # Brute-force attack options
    brute_group = parser.add_argument_group('Brute-force Attack Options')
    brute_group.add_argument(
        '-b', '--brute',
        help="Enable brute-force attack mode",
        action='store_true'
    )
    brute_group.add_argument(
        '-u', '--uppercase',
        help="Include uppercase letters (A-Z) in brute-force",
        action='store_true'
    )
    brute_group.add_argument(
        '-l', '--lowercase',
        help="Include lowercase letters (a-z) in brute-force",
        action='store_true'
    )
    brute_group.add_argument(
        '-n', '--digits',
        help="Include digits (0-9) in brute-force",
        action='store_true'
    )
    brute_group.add_argument(
        '-s', '--symbols',
        help="Include special symbols in brute-force",
        action='store_true'
    )
    brute_group.add_argument(
        '-m', '--max-length',
        help="Maximum password length for brute-force (default: 8, max recommended: 10)",
        default=8,
        type=int,
        metavar='N'
    )

    # Performance options
    perf_group = parser.add_argument_group('Performance Options')
    perf_group.add_argument(
        '-t', '--threads',
        help="Number of parallel processes to use (default: CPU count). Set to 1 to disable multiprocessing",
        type=int,
        default=None,
        metavar='N'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.dictionary and not args.brute:
        parser.error("At least one attack mode must be specified: -d (dictionary) or -b (brute-force)")

    if args.brute:
        if not any([args.uppercase, args.lowercase, args.digits, args.symbols]):
            parser.error("Brute-force mode requires at least one character set: -u, -l, -n, or -s")

        if args.max_length < 1:
            parser.error("Maximum length must be at least 1")

        if args.max_length > 16:
            parser.error("Maximum length cannot exceed 16 (computational limit)")

    if args.threads is not None and args.threads < 1:
        parser.error("Number of threads must be at least 1")

    return args


def validate_file(file_path: str) -> None:
    """
    Validate that the target file exists and is accessible.

    Args:
        file_path: Path to the archive file

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not a supported format
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archive file not found: {file_path}")

    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")

    # Check file extension (will raise ValueError if unsupported)
    _, ext = os.path.splitext(file_path.lower())
    if ext not in ['.rar', '.zip', '.7z']:
        raise ValueError(f"Unsupported file format: {ext}. Supported formats: .rar, .zip, .7z")


def main():
    """
    Main execution function.

    Orchestrates the password cracking process based on command-line arguments.
    """
    # Parse arguments
    try:
        args = parse_arguments()
    except SystemExit:
        return

    # Print banner
    print("=" * 70)
    print("  Brute Force Unpackage - Archive Password Cracker")
    print("  Supports: RAR, ZIP, 7Z")
    print("=" * 70)
    print()

    # Validate input file
    try:
        validate_file(args.file)
        print(f"[INFO] Target file: {args.file}")
        print(f"[INFO] File size: {os.path.getsize(args.file) / 1024:.2f} KB")
    except (FileNotFoundError, ValueError) as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)

    # Get appropriate archive handler
    try:
        archive_handler = get_handler_for_file(args.file)
        print(f"[INFO] Detected format: {archive_handler.get_format_name()}")
    except ValueError as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)

    # Determine multiprocessing settings
    use_multiprocess = args.threads is None or args.threads > 1
    num_processes = args.threads

    print(f"[INFO] Multiprocessing: {'Enabled' if use_multiprocess else 'Disabled'}")
    if use_multiprocess and num_processes:
        print(f"[INFO] Number of processes: {num_processes}")

    print()
    print("-" * 70)

    found_password = None

    # Execute dictionary attack if enabled
    if args.dictionary:
        print("\n[PHASE 1] Dictionary Attack")
        print("-" * 70)

        try:
            attacker = DictionaryAttacker(dictionary_path=args.dict_path)
            found_password = attacker.attack_file(
                args.file,
                archive_handler,
                use_multiprocess=use_multiprocess,
                num_processes=num_processes
            )
        except FileNotFoundError as e:
            print(f"[ERROR] {str(e)}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n[INTERRUPTED] Dictionary attack cancelled by user")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Dictionary attack failed: {str(e)}")

        if found_password:
            print_success(found_password)
            return

    # Execute brute-force attack if enabled and password not yet found
    if args.brute and not found_password:
        print("\n[PHASE 2] Brute-force Attack")
        print("-" * 70)

        try:
            attacker = BruteforceAttacker(
                include_uppercase=args.uppercase,
                include_lowercase=args.lowercase,
                include_digits=args.digits,
                include_symbols=args.symbols,
                max_length=args.max_length
            )
            found_password = attacker.attack_file(
                args.file,
                archive_handler,
                use_multiprocess=use_multiprocess,
                num_processes=num_processes
            )
        except ValueError as e:
            print(f"[ERROR] {str(e)}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n[INTERRUPTED] Brute-force attack cancelled by user")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Brute-force attack failed: {str(e)}")

        if found_password:
            print_success(found_password)
            return

    # Final result
    print("\n" + "=" * 70)
    if found_password:
        print_success(found_password)
    else:
        print("[RESULT] Password not found with current settings")
        print("[TIP] Try expanding your search:")
        print("  - Use more comprehensive dictionaries")
        print("  - Increase max-length for brute-force")
        print("  - Enable more character sets (uppercase, symbols, etc.)")
    print("=" * 70)


def print_success(password: str):
    """
    Print success message with the found password.

    Args:
        password: The cracked password
    """
    print()
    print("=" * 70)
    print("  SUCCESS! Password Found!")
    print("=" * 70)
    print(f"  Password: {password}")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
