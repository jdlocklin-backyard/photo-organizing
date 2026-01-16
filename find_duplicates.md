# Find Duplicates

A tool to scan folders for duplicate photos based on file type, size, and name similarity.

## Requirements

- Python 3.10+

## How to Use

1. Run the script:
   ```
   python find_duplicates.py
   ```

2. Select the folder to scan

3. Optionally select a folder to exclude

4. Review the duplicate groups found

## How Duplicates Are Detected

The script looks for files **within the same folder** that have:

- **Same file type** (extension)
- **Same file size**
- **80%+ filename similarity** (e.g., `IMG_001.jpg` and `IMG_001_copy.jpg`)

## Example Output

```
[Group 1] Folder: D:\Photos\2024
File type: JPG | Size: 5.2 MB
Files:
  - IMG_001.jpg
  - IMG_001_copy.jpg
  - IMG_001_edited.jpg
```

## Tips

- Review duplicates before deleting manually
- Files must match ALL criteria (type, size, AND similar name)
- The 80% threshold catches common duplicate patterns like `_copy`, `_1`, `(1)`, etc.
- Files with "final" in the name are automatically excluded
