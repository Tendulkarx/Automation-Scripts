import os
import time

from os.path import join, getsize
from heapq import nlargest


def walk_files_and_sizes(start_at: str):
    for root, _, files in os.walk(start_at):
        for file in files:
            path = join(root, file)
            try:
                size = getsize(path)  # bytes
                yield path, size
            except OSError:
                continue


def largest_files(n: int, start_at: str) -> None:
    MB = 1024 * 1024
    largest = nlargest(n, walk_files_and_sizes(start_at), key=lambda x: x[1])

    for path, size in largest:
        head, tail = os.path.split(path)
        print(f"{size // MB:05} MB {tail} {path}")


if __name__ == "__main__":
    start = time.perf_counter()
    largest_files(20, "/Users/sukobl/downloads")
    elapsed = time.perf_counter() - start
    print(f"{elapsed} seconds elapsed")
