"""
Brute-force password attack implementation.

This module implements brute-force attacks by generating all possible
password combinations from a specified character set.
"""

from itertools import product
from typing import List
from src.core.base_attacker import BaseAttacker


class BruteforceAttacker(BaseAttacker):
    """
    Brute-force password attack implementation.

    This class generates password candidates by creating all possible
    combinations of specified character sets up to a maximum length.
    """

    # Character set definitions
    UPPERCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LOWERCASE_LETTERS = "abcdefghijklmnopqrstuvwxyz"
    DIGITS = "0123456789"
    SPECIAL_SYMBOLS = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    def __init__(self,
                 include_uppercase: bool = True,
                 include_lowercase: bool = True,
                 include_digits: bool = True,
                 include_symbols: bool = False,
                 max_length: int = 8):
        """
        Initialize brute-force attacker.

        Args:
            include_uppercase: Include uppercase letters (A-Z)
            include_lowercase: Include lowercase letters (a-z)
            include_digits: Include digits (0-9)
            include_symbols: Include special symbols
            max_length: Maximum password length to attempt
        """
        super().__init__()

        self.include_uppercase = include_uppercase
        self.include_lowercase = include_lowercase
        self.include_digits = include_digits
        self.include_symbols = include_symbols
        self.max_length = max_length

        # Build character set
        self.charset = self._build_charset()

        if not self.charset:
            raise ValueError("At least one character set must be enabled")

        if max_length < 1:
            raise ValueError("Maximum length must be at least 1")

        if max_length > 16:
            print("[WARNING] Maximum length > 16 may take extremely long time")

        print(f"[INFO] Brute-force character set: {self.charset}")
        print(f"[INFO] Character set size: {len(self.charset)}")
        print(f"[INFO] Maximum password length: {max_length}")

        # Calculate total combinations
        total_combinations = sum(len(self.charset) ** i for i in range(1, max_length + 1))
        print(f"[WARNING] Total password combinations to attempt: {total_combinations:,}")

    def _build_charset(self) -> str:
        """
        Build the character set based on enabled options.

        Returns:
            String containing all enabled characters
        """
        charset = ""

        if self.include_uppercase:
            charset += self.UPPERCASE_LETTERS

        if self.include_lowercase:
            charset += self.LOWERCASE_LETTERS

        if self.include_digits:
            charset += self.DIGITS

        if self.include_symbols:
            charset += self.SPECIAL_SYMBOLS

        return charset

    def generate_passwords_of_length(self, length: int) -> List[str]:
        """
        Generate all password combinations of a specific length.

        Args:
            length: Length of passwords to generate

        Returns:
            List of all possible passwords of the given length
        """
        return [''.join(combo) for combo in product(self.charset, repeat=length)]

    def generate_passwords(self) -> List[str]:
        """
        Generate all password candidates up to max_length.

        This method generates passwords incrementally from length 1 to max_length.
        For memory efficiency, this is typically used with generators in practice.

        Returns:
            List of all password candidates
        """
        all_passwords = []

        for length in range(1, self.max_length + 1):
            all_passwords.extend(self.generate_passwords_of_length(length))

        return all_passwords

    def attack_file(self, file_path: str, archive_handler, use_multiprocess: bool = False,
                    num_processes: int = None) -> str:
        """
        Perform brute-force attack on archive file.

        Args:
            file_path: Path to the encrypted archive
            archive_handler: Archive format handler
            use_multiprocess: Whether to use multiprocessing
            num_processes: Number of processes (if using multiprocessing)

        Returns:
            The correct password if found, None otherwise
        """
        print(f"[INFO] Starting brute-force attack on {file_path}")
        print(f"[INFO] Archive format: {archive_handler.get_format_name()}")

        if use_multiprocess:
            from src.core.multiprocess_attacker import MultiprocessAttacker

            # For brute-force, we process length by length
            mp_attacker = MultiprocessAttacker(num_processes)

            for length in range(1, self.max_length + 1):
                print(f"\n[INFO] Attempting passwords of length {length}")
                passwords = self.generate_passwords_of_length(length)
                print(f"[INFO] Generated {len(passwords):,} password candidates")

                result = mp_attacker.attack(file_path, passwords, archive_handler)
                if result:
                    return result

            return None
        else:
            # Single-process mode: try passwords incrementally by length
            for length in range(1, self.max_length + 1):
                print(f"\n[INFO] Attempting passwords of length {length}")
                passwords = self.generate_passwords_of_length(length)
                print(f"[INFO] Generated {len(passwords):,} password candidates")

                result = self.attack(file_path, archive_handler, passwords)
                if result:
                    return result

            return None
