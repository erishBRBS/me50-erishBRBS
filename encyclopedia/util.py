from pathlib import Path
import random
import re

BASE_DIR = Path(__file__).resolve().parent.parent
ENTRIES_DIR = BASE_DIR / 'entries'


def list_entries():
    dirpath, dirnames, filenames = next(Path(ENTRIES_DIR).walk())
    print("dirpath:", dirpath)
    print("dirnames:", dirnames)
    print("filenames:", filenames)
    return sorted(re.sub(r'\.md$', '', filename) for filename in filenames if filename.endswith('.md'))


def save_entry(title, content):
    filename = ENTRIES_DIR / f"{title}.md"
    filename.write_text(content, encoding='utf-8')


def get_entry(title):
    filename = ENTRIES_DIR / f"{title}.md"
    if filename.exists():
        return filename.read_text(encoding='utf-8')
    return None


def get_random_entry():
    entries = list_entries()
    return random.choice(entries) if entries else None
