# photo-organizing User Guide

This guide explains what each file in this repository does and how to use the scripts safely.

## Repository Overview

This repository contains three Python utilities for managing a photo library:

1. **`scripts/organize_photos.py`** - Organizes photos and videos into date-based folders
2. **`scripts/find_duplicates.py`** - Finds likely duplicate files in the same folder
3. **`scripts/delete_empty_folders.py`** - Removes junk files and deletes empty folders

The repository also includes Markdown help files for each script:

- `docs/organize_photos.md`
- `docs/find_duplicates.md`
- `docs/delete_empty_folders.md`

## Requirements

- Python 3.10 or newer
- Dependencies from `requirements.txt`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Before You Start

Before running any script:

1. Make a backup of your photos.
2. Test on a small folder first.
3. Prefer **copy** options before **move** options when available.
4. Review results before deleting anything.

## File-by-File Guide

### 1. `scripts/organize_photos.py`

**Purpose:**
Organizes photos and videos into folders based on date.

**How it works:**
- Scans a source folder
- Reads date information from EXIF metadata when available
- Falls back to file creation date when needed
- Sorts files into folders by year, then date, then file type

**Example output structure:**

```text
Organized/
└── 2026/
    └── 20260112/
        ├── JPG/
        ├── NEF/
        ├── RAF/
        └── MOV/
```

**How to run:**

```bash
python scripts/organize_photos.py
```

**Recommended workflow:**
1. Select the folder containing your photos.
2. Choose a destination folder.
3. Choose **Copy** first to verify results.
4. Confirm the operation.
5. Review the organized output.
6. Use **Move** only after you trust the results.

**Supported file types:**
- Images: JPG, JPEG, PNG, GIF, BMP, TIFF, TIF, WEBP, HEIC, HEIF
- RAW: NEF, ARW, CR2, DNG, RAF, ORF, RW2, PEF, SRW, RAW
- Video: AVI, MOV
- Other: PSD, XMP

**Date handling notes:**
- RAW files use EXIF “Date Taken” when available.
- JPG, CR2, PNG, and XMP may use the date from a matching RAW file with the same filename.
- Other files use EXIF date if present, otherwise file creation date.

**Tips:**
- Keep RAW and JPG pairs together so dates stay aligned.
- Use a test folder before processing your full library.

---

### 2. `scripts/find_duplicates.py`

**Purpose:**
Finds likely duplicate photos within the same folder.

**How it works:**
Files are grouped as duplicates only when they match all of the following:
- Same file type/extension
- Same file size
- 80% or greater filename similarity

Files with `final` in the name are excluded automatically.

**How to run:**

```bash
python scripts/find_duplicates.py
```

**Recommended workflow:**
1. Select the folder to scan.
2. Optionally choose a folder to exclude.
3. Review the duplicate groups shown.
4. Manually decide what to keep or delete.

**Example duplicate group:**

```text
[Group 1] Folder: D:\Photos\2024
File type: JPG | Size: 5.2 MB
Files:
  - IMG_001.jpg
  - IMG_001_copy.jpg
  - IMG_001_edited.jpg
```

**Tips:**
- This script helps identify likely duplicates, but you should review them manually.
- Do not delete files automatically unless you have confirmed they are true duplicates.

---

### 3. `scripts/delete_empty_folders.py`

**Purpose:**
Cleans up junk files and removes empty folders.

**What it deletes:**
- `.Bridge*` files
- `.picas*` files
- `.bak*` files

It also removes empty folders recursively.

**How to run:**

```bash
python scripts/delete_empty_folders.py
```

**Recommended workflow:**
1. Select the folder to scan.
2. Review junk files found in Phase 1.
3. Confirm deletion if the preview looks correct.
4. Review empty folders found in Phase 2.
5. Confirm deletion.

**Tips:**
- Run this after organizing your photo library.
- The script may repeat scanning until all empty folders are removed.
- Review every preview carefully before confirming.

## Suggested End-to-End Workflow

If you are cleaning up a large photo collection, use the tools in this order:

1. **Organize files** with `scripts/organize_photos.py`
2. **Review for duplicates** with `scripts/find_duplicates.py`
3. **Clean up leftovers** with `scripts/delete_empty_folders.py`

## Included Documentation Files

These files are quick references for each script:

- `docs/organize_photos.md` - script-specific usage notes
- `docs/find_duplicates.md` - duplicate detection details
- `docs/delete_empty_folders.md` - cleanup behavior and confirmations

## Troubleshooting

### Python is not recognized
Make sure Python 3.10+ is installed and available in your terminal.

### Pillow import errors
Reinstall dependencies:

```bash
pip install -r requirements.txt
```

### Wrong dates or unexpected folder placement
- Check whether the files contain EXIF date information.
- Keep related RAW and JPG files in the same folder.
- Test with **Copy** mode first.

### Too many duplicate matches
Remember that duplicate detection is based on filename similarity, file size, and extension. Review matches manually.

## Safety Reminders

- Always keep a backup before processing a large library.
- Use **Copy** before **Move**.
- Review duplicate and deletion previews carefully.
- Start with a small sample folder before using these scripts on your full archive.
