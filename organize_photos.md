# Photo Organizer

A simple tool to organize your photos and videos into date-based folders.

## Folder Structure

Photos are organized as:
```
Organized/
└── 2026/
    └── 20260112/
        ├── JPG/
        ├── NEF/
        ├── RAF/
        └── MOV/
```

## Requirements

- Python 3.10+
- Pillow library

## Installation

```
pip install -r requirements.txt
```

## How to Use

1. Run the script:
   ```
   python organize_photos.py
   ```

2. Select the folder containing your photos

3. Choose a destination folder (or use the default "Organized" folder)

4. Choose to **Copy** (keeps originals) or **Move** (removes originals)

5. Confirm to start organizing

## Supported File Types

| Type | Extensions |
|------|------------|
| Images | JPG, JPEG, PNG, GIF, BMP, TIFF, TIF, WEBP, HEIC, HEIF |
| RAW | NEF, ARW, CR2, DNG, RAF, ORF, RW2, PEF, SRW, RAW |
| Video | AVI, MOV |
| Other | PSD, XMP |

## How Dates Are Determined

- **RAW files** (NEF, ARW, DNG, RAF, etc.): Uses "Date Taken" from EXIF data
- **JPG, CR2, PNG, XMP**: Uses the date from the matching RAW file (same filename), or file creation date if no RAW exists
- **Other files**: Uses EXIF "Date Taken" if available, otherwise file creation date

## Tips

- Keep RAW and JPG pairs in the same folder so JPGs inherit the correct date
- Use **Copy** first to verify results before using **Move**
