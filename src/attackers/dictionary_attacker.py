"""
Dictionary-based password attack implementation.

This module implements brute-force attacks using pre-compiled password dictionaries.
"""

import os
from typing import List
from src.core.base_attacker import BaseAttacker


class DictionaryAttacker(BaseAttacker):
    """
    Dictionary-based password attack implementation.

    This class loads passwords from text files in a specified directory
    and attempts them against an encrypted archive.
    """

    def __init__(self, dictionary_path: str = "password_list"):
        """
        Initialize dictionary attacker.

        Args:
            dictionary_path: Path to directory containing password dictionary files
        """
        super().__init__()
        self.dictionary_path = dictionary_path
        self.passwords: List[str] = []
        self._load_dictionaries()

    def _load_dictionaries(self) -> None:
        """
        Load all password dictionaries from the specified path.

        Recursively walks through the dictionary directory and loads all .txt files,
        storing unique passwords in memory.
        """
        if not os.path.exists(self.dictionary_path):
            raise FileNotFoundError(f"Dictionary path not found: {self.dictionary_path}")

        if not os.path.isdir(self.dictionary_path):
            raise ValueError(f"Dictionary path must be a directory: {self.dictionary_path}")

        password_set = set()  # Use set to avoid duplicates

        print(f"[INFO] Loading dictionaries from: {self.dictionary_path}")

        for root, dirs, files in os.walk(self.dictionary_path):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                password = line.strip()
                                if password:  # Skip empty lines
                                    password_set.add(password)
                    except Exception as e:
                        print(f"[WARNING] Failed to load {file_path}: {str(e)}")
                        continue

        self.passwords = list(password_set)
        print(f"[INFO] Loaded {len(self.passwords)} unique passwords from dictionaries")

    def generate_passwords(self) -> List[str]:
        """
        Return the loaded dictionary passwords.

        Returns:
            List of password candidates from dictionaries
        """
        return self.passwords

    def attack_file(self, file_path: str, archive_handler, use_multiprocess: bool = False,
                    num_processes: int = None) -> str:
        """
        Perform dictionary attack on archive file.

        Args:
            file_path: Path to the encrypted archive
            archive_handler: Archive format handler
            use_multiprocess: Whether to use multiprocessing
            num_processes: Number of processes (if using multiprocessing)

        Returns:
            The correct password if found, None otherwise
        """
        if not self.passwords:
            print("[ERROR] No passwords loaded from dictionaries")
            return None

        print(f"[INFO] Starting dictionary attack on {file_path}")
        print(f"[INFO] Archive format: {archive_handler.get_format_name()}")
        print(f"[INFO] Total passwords to attempt: {len(self.passwords)}")

        if use_multiprocess:
            from src.core.multiprocess_attacker import MultiprocessAttacker
            mp_attacker = MultiprocessAttacker(num_processes)
            return mp_attacker.attack(file_path, self.passwords, archive_handler)
        else:
            return self.attack(file_path, archive_handler, self.passwords)
