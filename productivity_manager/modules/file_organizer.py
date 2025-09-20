import hashlib
import os
import shutil
from typing import Dict, List, Tuple, DefaultDict
from collections import defaultdict

from ..utils.constants import FILE_CATEGORIES


def hash_file(path: str, block_size: int = 1024 * 1024) -> str:
    """Compute SHA-256 for a file using a larger block size for speed.

    Uses 1MB blocks to reduce the number of read() syscalls compared to the
    previous 64KB default, typically improving throughput on modern disks.
    """
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            h.update(chunk)
    return h.hexdigest()


def organize_directory(directory: str) -> List[str]:
    """Organize files by extension into category folders (non-recursive).

    Optimized by precomputing an extension->category map to avoid scanning all
    categories per file.
    """
    logs: List[str] = []
    if not os.path.isdir(directory):
        return [f"Directory not found: {directory}"]

    # Precompute extension -> category map once
    ext_to_cat: Dict[str, str] = {
        ext.lower(): cat for cat, exts in FILE_CATEGORIES.items() for ext in exts
    }

    for entry in os.scandir(directory):
        if not entry.is_file():
            continue
        _, ext = os.path.splitext(entry.name)
        ext = ext.lower()
        target_category = ext_to_cat.get(ext, "Other")
        target_dir = os.path.join(directory, target_category)
        os.makedirs(target_dir, exist_ok=True)
        dest = os.path.join(target_dir, entry.name)
        # avoid overwrite
        base, ext2 = os.path.splitext(entry.name)
        counter = 1
        while os.path.exists(dest):
            dest = os.path.join(target_dir, f"{base} ({counter}){ext2}")
            counter += 1
        shutil.move(entry.path, dest)
        logs.append(f"Moved: {entry.name} -> {os.path.relpath(dest, directory)}")
    return logs


def find_duplicates(directory: str) -> List[Tuple[str, List[str]]]:
    """Find duplicate files by content efficiently.

    Strategy:
      1) Group files by size (cheap) and discard unique sizes.
      2) Within same-size groups, group by a quick partial-hash of the first 256KB.
      3) For groups still with >1 file, compute full SHA-256 and report duplicates.
    """
    # Step 1: group by file size
    size_groups: DefaultDict[int, List[str]] = defaultdict(list)
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            try:
                sz = os.path.getsize(path)
            except Exception:
                continue
            size_groups[sz].append(path)

    # Step 2: partial-hash groups
    def partial_hash(path: str, nbytes: int = 256 * 1024) -> str:
        h = hashlib.sha256()
        try:
            with open(path, 'rb') as f:
                chunk = f.read(nbytes)
                h.update(chunk)
            return h.hexdigest()
        except Exception:
            return ''  # unreadable files fall into their own bucket and will be ignored later

    candidates: List[List[str]] = []
    for sz, paths in size_groups.items():
        if len(paths) <= 1:
            continue
        by_partial: DefaultDict[str, List[str]] = defaultdict(list)
        for p in paths:
            by_partial[partial_hash(p)].append(p)
        for group in by_partial.values():
            if len(group) > 1:
                candidates.append(group)

    # Step 3: full hash groups and collect duplicates
    full_hashes: DefaultDict[str, List[str]] = defaultdict(list)
    for group in candidates:
        for p in group:
            try:
                h = hash_file(p)
                full_hashes[h].append(p)
            except Exception:
                # Skip unreadable files
                continue

    return [(h, paths) for h, paths in full_hashes.items() if len(paths) > 1]


def batch_rename(directory: str, pattern: str = "file_{index}") -> List[str]:
    logs: List[str] = []
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for idx, name in enumerate(files, start=1):
        _, ext = os.path.splitext(name)
        new_name = f"{pattern.format(index=idx)}{ext}"
        src = os.path.join(directory, name)
        dst = os.path.join(directory, new_name)
        counter = 1
        while os.path.exists(dst):
            dst = os.path.join(directory, f"{pattern.format(index=idx)}_{counter}{ext}")
            counter += 1
        os.rename(src, dst)
        logs.append(f"Renamed: {name} -> {os.path.basename(dst)}")
    return logs
