import hashlib
import os
import shutil
from typing import Dict, List, Tuple

from utils.constants import FILE_CATEGORIES


def hash_file(path: str, block_size: int = 65536) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            h.update(chunk)
    return h.hexdigest()


def organize_directory(directory: str) -> List[str]:
    logs: List[str] = []
    if not os.path.isdir(directory):
        return [f"Directory not found: {directory}"]
    for entry in os.scandir(directory):
        if not entry.is_file():
            continue
        _, ext = os.path.splitext(entry.name)
        ext = ext.lower()
        target_category = None
        for cat, exts in FILE_CATEGORIES.items():
            if ext in exts:
                target_category = cat
                break
        if not target_category:
            target_category = "Other"
        target_dir = os.path.join(directory, target_category)
        os.makedirs(target_dir, exist_ok=True)
        dest = os.path.join(target_dir, entry.name)
        # avoid overwrite
        base, ext = os.path.splitext(entry.name)
        counter = 1
        while os.path.exists(dest):
            dest = os.path.join(target_dir, f"{base} ({counter}){ext}")
            counter += 1
        shutil.move(entry.path, dest)
        logs.append(f"Moved: {entry.name} -> {os.path.relpath(dest, directory)}")
    return logs


def find_duplicates(directory: str) -> List[Tuple[str, List[str]]]:
    hashes: Dict[str, List[str]] = {}
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            try:
                h = hash_file(path)
                hashes.setdefault(h, []).append(path)
            except Exception:
                continue
    return [(h, paths) for h, paths in hashes.items() if len(paths) > 1]


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

