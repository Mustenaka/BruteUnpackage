"""
Base attacker class providing common functionality for brute-force attacks.

This module contains the abstract base class for all password attack implementations,
defining the common interface and shared logic.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from tqdm import tqdm


class BaseAttacker(ABC):
    """
    Abstract base class for password brute-force attacks.

    This class provides the common framework for both dictionary-based and
    brute-force password attacks on compressed archives.
    """

    def __init__(self):
        """Initialize the base attacker."""
        self.found_password: Optional[str] = None

    @abstractmethod
    def generate_passwords(self) -> List[str]:
        """
        Generate a list of passwords to attempt.

        Returns:
            List[str]: List of password candidates
        """
        pass

    def attack(self, file_path: str, archive_handler, password_candidates: List[str]) -> Optional[str]:
        """
        Perform brute-force attack on an archive file.

        Args:
            file_path: Path to the archive file
            archive_handler: Archive format handler (strategy pattern)
            password_candidates: List of passwords to try

        Returns:
            The correct password if found, None otherwise
        """
        tbar = tqdm(password_candidates, desc="Attempting passwords")

        for password in tbar:
            tbar.set_description(f'Trying: {password[:20]}...' if len(password) > 20 else f'Trying: {password}')

            try:
                # Attempt to extract the archive with the current password
                if archive_handler.try_extract(file_path, password):
                    self.found_password = password
                    print(f"\n[SUCCESS] Password found: {password}")
                    return password
            except KeyboardInterrupt:
                print("\n[INTERRUPTED] Attack stopped by user")
                raise
            except Exception:
                # Continue to next password on failure
                continue

        print("\n[FAILED] Password not found in provided candidates")
        return None
