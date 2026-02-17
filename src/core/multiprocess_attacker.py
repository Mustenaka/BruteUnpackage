"""
Multiprocessing support for parallel password cracking.

This module implements multiprocessing functionality to bypass Python's GIL
and maximize CPU utilization across multiple cores.
"""

import multiprocessing as mp
from typing import List, Optional, Callable
import os
import math
from tqdm import tqdm


def worker_attack(file_path: str, password_chunk: List[str], archive_handler_class: type,
                  queue: mp.Queue, worker_id: int) -> None:
    """
    Worker process that attempts passwords from its assigned chunk.

    Args:
        file_path: Path to the archive file
        password_chunk: List of passwords this worker should attempt
        archive_handler_class: Class of the archive handler to use
        queue: Multiprocessing queue to report results
        worker_id: ID of this worker process
    """
    try:
        # Each worker creates its own handler instance
        handler = archive_handler_class()

        for password in password_chunk:
            try:
                if handler.try_extract(file_path, password):
                    # Password found! Report to main process
                    queue.put(('found', password, worker_id))
                    return
            except Exception:
                continue

        # This worker finished without finding password
        queue.put(('done', None, worker_id))

    except Exception as e:
        queue.put(('error', str(e), worker_id))


class MultiprocessAttacker:
    """
    Manages multiprocessing-based password cracking attacks.

    This class distributes password candidates across multiple processes
    to maximize CPU utilization and bypass Python's GIL limitation.
    """

    def __init__(self, num_processes: Optional[int] = None):
        """
        Initialize multiprocess attacker.

        Args:
            num_processes: Number of processes to use. If None, uses CPU count.
        """
        if num_processes is None:
            self.num_processes = mp.cpu_count()
        else:
            self.num_processes = max(1, min(num_processes, mp.cpu_count()))

        print(f"[INFO] Using {self.num_processes} processes for parallel attack")

    def split_passwords(self, passwords: List[str]) -> List[List[str]]:
        """
        Divide password list into chunks for each process.

        Args:
            passwords: Complete list of password candidates

        Returns:
            List of password chunks, one for each process
        """
        chunk_size = math.ceil(len(passwords) / self.num_processes)
        chunks = []

        for i in range(self.num_processes):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(passwords))
            if start_idx < len(passwords):
                chunks.append(passwords[start_idx:end_idx])

        return chunks

    def attack(self, file_path: str, passwords: List[str], archive_handler) -> Optional[str]:
        """
        Perform parallel brute-force attack using multiprocessing.

        Args:
            file_path: Path to the archive file
            passwords: List of all password candidates
            archive_handler: Archive handler instance (used to get class type)

        Returns:
            The correct password if found, None otherwise
        """
        if not passwords:
            print("[ERROR] No passwords to attempt")
            return None

        # Split passwords into chunks
        password_chunks = self.split_passwords(passwords)

        # Create result queue
        result_queue = mp.Queue()

        # Create and start worker processes
        processes = []
        handler_class = type(archive_handler)

        print(f"[INFO] Distributing {len(passwords)} passwords across {len(password_chunks)} processes")

        for i, chunk in enumerate(password_chunks):
            p = mp.Process(
                target=worker_attack,
                args=(file_path, chunk, handler_class, result_queue, i)
            )
            p.start()
            processes.append(p)

        # Monitor results
        found_password = None
        completed_workers = 0
        total_workers = len(processes)

        # Progress tracking
        with tqdm(total=len(passwords), desc="Overall progress") as pbar:
            while completed_workers < total_workers:
                try:
                    status, data, worker_id = result_queue.get(timeout=1)

                    if status == 'found':
                        found_password = data
                        print(f"\n[SUCCESS] Worker {worker_id} found password: {data}")
                        # Terminate all processes
                        for p in processes:
                            if p.is_alive():
                                p.terminate()
                        break

                    elif status == 'done':
                        completed_workers += 1
                        chunk_size = len(password_chunks[worker_id])
                        pbar.update(chunk_size)

                    elif status == 'error':
                        print(f"\n[WARNING] Worker {worker_id} encountered error: {data}")
                        completed_workers += 1

                except mp.queues.Empty:
                    # Update progress for alive processes
                    continue
                except KeyboardInterrupt:
                    print("\n[INTERRUPTED] Terminating all worker processes...")
                    for p in processes:
                        if p.is_alive():
                            p.terminate()
                    break

        # Wait for all processes to finish
        for p in processes:
            p.join(timeout=2)
            if p.is_alive():
                p.kill()

        if found_password:
            return found_password
        else:
            print("\n[FAILED] Password not found")
            return None
