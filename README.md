# photo-organizing

Simple Python tools for organizing and cleaning up a photo library.

## What This Repository Does

This project includes scripts to:

- organize photos and videos into date-based folders
- find likely duplicate files
- delete junk files and empty folders

## Project Structure

```text
photo-organizing/
├── README.md
├── requirements.txt
├── docs/
│   ├── user-guide.md
│   ├── organize_photos.md
│   ├── find_duplicates.md
│   └── delete_empty_folders.md
├── scripts/
│   ├── organize_photos.py
│   ├── find_duplicates.py
│   └── delete_empty_folders.py
```

## Requirements

- Python 3.10+
- Dependencies from `requirements.txt`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Quick Start

Run the scripts from the repository root:

```bash
python scripts/organize_photos.py
python scripts/find_duplicates.py
python scripts/delete_empty_folders.py
```

## Documentation

- [User Guide](docs/user-guide.md)
- [Organize Photos](docs/organize_photos.md)
- [Find Duplicates](docs/find_duplicates.md)
- [Delete Empty Folders](docs/delete_empty_folders.md)

## Recommended Workflow

1. Organize files with `scripts/organize_photos.py`
2. Review duplicates with `scripts/find_duplicates.py`
3. Clean up leftovers with `scripts/delete_empty_folders.py`
