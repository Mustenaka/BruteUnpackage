"""
Archive format handlers using strategy pattern.

This module contains handler classes for different archive formats (RAR, ZIP, 7Z).
Each handler implements the same interface for password extraction attempts.
"""

from abc import ABC, abstractmethod
from zipfile import ZipFile
import py7zr
import os
import tempfile

# Try to import UnRAR library, handle gracefully if not available
try:
    from unrar import rarfile
    UNRAR_AVAILABLE = True
except (ImportError, LookupError):
    UNRAR_AVAILABLE = False
    rarfile = None


class ArchiveHandler(ABC):
    """Abstract base class for archive format handlers."""

    @abstractmethod
    def try_extract(self, file_path: str, password: str) -> bool:
        """
        Attempt to extract archive with given password.

        Args:
            file_path: Path to the archive file
            password: Password to attempt

        Returns:
            True if extraction succeeded, False otherwise
        """
        pass

    @abstractmethod
    def get_format_name(self) -> str:
        """
        Get the name of the archive format.

        Returns:
            String representation of the format (e.g., 'RAR', 'ZIP')
        """
        pass


class RARHandler(ArchiveHandler):
    """Handler for RAR archive format."""

    def __init__(self):
        """Initialize RAR handler and check for UnRAR library."""
        if not UNRAR_AVAILABLE:
            raise RuntimeError(
                "UnRAR library is not available. Please install it:\n"
                "  1. Install libunrar: brew install libunrar (macOS)\n"
                "  2. Set UNRAR_LIB_PATH environment variable\n"
                "  See README.md for detailed instructions."
            )

    def try_extract(self, file_path: str, password: str) -> bool:
        """
        Attempt to extract RAR archive.

        Args:
            file_path: Path to the RAR file
            password: Password to attempt

        Returns:
            True if password is correct
        """
        try:
            with rarfile.RarFile(file_path) as rf:
                # Use temporary directory for testing extraction
                with tempfile.TemporaryDirectory() as temp_dir:
                    rf.extractall(path=temp_dir, pwd=password)
                return True
        except (rarfile.BadRarFile, rarfile.PasswordRequired, RuntimeError):
            return False
        except Exception:
            return False

    def get_format_name(self) -> str:
        """Return format name."""
        return "RAR"


class ZIPHandler(ArchiveHandler):
    """Handler for ZIP archive format."""

    def try_extract(self, file_path: str, password: str) -> bool:
        """
        Attempt to extract ZIP archive.

        Args:
            file_path: Path to the ZIP file
            password: Password to attempt

        Returns:
            True if password is correct
        """
        try:
            with ZipFile(file_path, 'r') as zip_ref:
                # Convert password to bytes if it's a string
                pwd_bytes = password.encode('utf-8') if isinstance(password, str) else password

                # Use temporary directory for testing extraction
                with tempfile.TemporaryDirectory() as temp_dir:
                    zip_ref.extractall(path=temp_dir, pwd=pwd_bytes)
                return True
        except (RuntimeError, Exception):
            return False

    def get_format_name(self) -> str:
        """Return format name."""
        return "ZIP"


class SevenZHandler(ArchiveHandler):
    """Handler for 7Z archive format."""

    def try_extract(self, file_path: str, password: str) -> bool:
        """
        Attempt to extract 7Z archive.

        Args:
            file_path: Path to the 7Z file
            password: Password to attempt

        Returns:
            True if password is correct
        """
        try:
            with py7zr.SevenZipFile(file_path, mode='r', password=password) as z:
                # Use temporary directory for testing extraction
                with tempfile.TemporaryDirectory() as temp_dir:
                    z.extractall(path=temp_dir)
                return True
        except Exception:
            return False

    def get_format_name(self) -> str:
        """Return format name."""
        return "7Z"


def get_handler_for_file(file_path: str) -> ArchiveHandler:
    """
    Factory function to get appropriate handler based on file extension.

    Args:
        file_path: Path to the archive file

    Returns:
        Appropriate ArchiveHandler instance

    Raises:
        ValueError: If file extension is not supported
        RuntimeError: If required library is not available
    """
    _, extension = os.path.splitext(file_path.lower())

    if extension not in ['.rar', '.zip', '.7z']:
        raise ValueError(
            f"Unsupported archive format: {extension}\n"
            f"Supported formats: .rar, .zip, .7z"
        )

    # Create handler based on extension
    if extension == '.rar':
        return RARHandler()
    elif extension == '.zip':
        return ZIPHandler()
    elif extension == '.7z':
        return SevenZHandler()
    else:
        raise ValueError(f"Unsupported archive format: {extension}")
