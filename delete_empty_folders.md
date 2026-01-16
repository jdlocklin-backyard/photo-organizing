# Delete Empty Folders

A simple tool to clean up junk files and delete empty folders.

## Requirements

- Python 3.10+

## How to Use

1. Run the script:
   ```
   python delete_empty_folders.py
   ```

2. Select the folder to scan

3. **Phase 1**: Review junk files found and confirm deletion

4. **Phase 2**: Review empty folders found and confirm deletion

## Features

- **Junk File Cleanup**: Deletes files matching these patterns:
  - `.Bridge*` (Adobe Bridge cache files)
  - `.picas*` (Picasa metadata files)
  - `.bak*` (Backup files)

- **Empty Folder Cleanup**:
  - Scans all subfolders recursively
  - Handles nested empty folders (deletes deepest first)
  - Shows preview before deleting

## Tips

- Run this after organizing photos to clean up source folders
- Each phase has its own confirmation dialog
- The script will keep scanning until no empty folders remain
