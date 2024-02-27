import hashlib
from pathlib import Path


def sha1checksum(filename: Path or str) -> str:
    h = hashlib.sha1()
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()
