"""
Duplicate Photo Finder Script
Scans folders for duplicate photos based on file size, type, and name similarity.
Only compares files within the same folder.
"""

import os
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
from tkinter import Tk, filedialog, messagebox


SIMILARITY_THRESHOLD = 0.80  # 80% similarity threshold


def select_folder(title: str = "Select Folder") -> str | None:
    """Open a folder selection dialog and return the selected path."""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.focus_force()
    root.update()
    
    folder_path = filedialog.askdirectory(title=title, parent=root)
    root.destroy()
    
    return folder_path if folder_path else None


def filename_similarity(name1: str, name2: str) -> float:
    """Calculate similarity ratio between two filenames (without extension)."""
    return SequenceMatcher(None, name1.lower(), name2.lower()).ratio()


def is_image_file(file_path: str) -> bool:
    """Check if a file is an image or media file based on extension."""
    image_extensions = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
        '.webp', '.heic', '.heif', '.raw', '.cr2', '.nef', '.arw',
        '.dng', '.orf', '.rw2', '.pef', '.srw', '.raf',
        '.psd', '.xmp',
        '.avi', '.mov', '.wmv'
    }
    return Path(file_path).suffix.lower() in image_extensions


def get_base_name(filename: str) -> str:
    """Get the base name without extension."""
    return Path(filename).stem


def find_duplicates_in_folder(folder_path: str) -> dict[str, list[str]]:
    """
    Find duplicate files within a single folder.
    Groups files by file size, extension, and filename similarity (80%+).
    
    Returns:
        Dictionary of duplicate groups
    """
    duplicates = {}
    
    # Group files by extension and size first
    size_ext_groups = defaultdict(list)
    
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if not os.path.isfile(file_path):
                continue
            
            if not is_image_file(file_path):
                continue
            
            # Skip files with "final" in the name
            if 'final' in filename.lower():
                continue
            
            extension = Path(filename).suffix.lower()
            file_size = os.path.getsize(file_path)
            base_name = get_base_name(filename)
            
            # Group by extension and size
            key = (extension, file_size)
            size_ext_groups[key].append({
                'path': file_path,
                'filename': filename,
                'base_name': base_name,
                'size': file_size,
                'extension': extension
            })
    except PermissionError:
        pass
    
    # Find groups with multiple files and check filename similarity
    group_counter = 0
    for (extension, size), files in size_ext_groups.items():
        if len(files) > 1:
            # Check filename similarity within each size/extension group
            processed = set()
            
            for i, file1 in enumerate(files):
                if i in processed:
                    continue
                
                similar_files = [file1]
                processed.add(i)
                
                for j, file2 in enumerate(files):
                    if j in processed:
                        continue
                    
                    similarity = filename_similarity(file1['base_name'], file2['base_name'])
                    if similarity >= SIMILARITY_THRESHOLD:
                        similar_files.append(file2)
                        processed.add(j)
                
                # Only report if we found duplicates (more than 1 file)
                if len(similar_files) > 1:
                    group_counter += 1
                    key = f"{folder_path}|{extension}|{size}|{group_counter}"
                    duplicates[key] = {
                        'folder': folder_path,
                        'extension': extension,
                        'size': size,
                        'files': similar_files
                    }
    
    return duplicates


def scan_for_duplicates(root_folder: str, excluded_folder: str | None = None) -> list[dict]:
    """
    Scan all folders for duplicates.
    
    Returns:
        List of duplicate groups found
    """
    all_duplicates = []
    
    # Normalize excluded path for comparison
    excluded_normalized = None
    if excluded_folder:
        excluded_normalized = os.path.normpath(os.path.abspath(excluded_folder)).lower()
    
    for root, dirs, files in os.walk(root_folder):
        # Skip excluded folder
        if excluded_normalized:
            root_normalized = os.path.normpath(os.path.abspath(root)).lower()
            if root_normalized == excluded_normalized or root_normalized.startswith(excluded_normalized + os.sep):
                continue
        
        folder_duplicates = find_duplicates_in_folder(root)
        
        for key, dup_info in folder_duplicates.items():
            all_duplicates.append(dup_info)
    
    return all_duplicates


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    """Main function to run the duplicate finder."""
    print("=" * 60)
    print("        DUPLICATE PHOTO FINDER")
    print("=" * 60)
    print("\nThis script will scan for duplicate photos based on:")
    print("  - Same file type (extension)")
    print("  - Same file size")
    print("\nOnly compares files within the same folder.\n")
    
    # Select folder to scan
    print("Please select the folder to scan...")
    folder_path = select_folder("Select folder to scan for duplicates")
    
    if not folder_path:
        print("No folder selected. Exiting.")
        return
    
    print(f"\nSelected folder: {folder_path}")
    
    # Ask if user wants to exclude a folder
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    exclude_folder = messagebox.askyesno(
        "Exclude Folder",
        "Do you want to exclude a folder from scanning?\n\n"
        "Click 'Yes' to select a folder to exclude\n"
        "Click 'No' to scan all folders"
    )
    root.destroy()
    
    excluded_folder = None
    if exclude_folder:
        print("Please select the folder to exclude...")
        excluded_folder = select_folder("Select folder to exclude")
        if excluded_folder:
            print(f"Excluded folder: {excluded_folder}")
        else:
            print("No folder excluded.")
    
    print("\nScanning for duplicates...")
    print("-" * 60)
    
    # Scan for duplicates
    duplicates = scan_for_duplicates(folder_path, excluded_folder)
    
    if not duplicates:
        print("\nNo duplicate photos found!")
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showinfo("Complete", "No duplicate photos found!")
        root.destroy()
        return
    
    # Count total duplicate groups
    total_groups = len(duplicates)
    total_files = sum(len(d['files']) for d in duplicates)
    
    print(f"\nFound {total_groups} group(s) with potential duplicates ({total_files} files total)")
    print("=" * 60)
    
    # Display duplicates
    for i, dup in enumerate(duplicates, 1):
        print(f"\n[Group {i}] Folder: {dup['folder']}")
        size_str = format_size(dup['size'])
        print(f"File type: {dup['extension'].upper()} | Size: {size_str}")
        print("Files:")
        
        for f in dup['files']:
            print(f"  - {f['filename']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("                  SUMMARY")
    print("=" * 60)
    print(f"Duplicate groups found: {total_groups}")
    print(f"Total files in groups: {total_files}")
    
    print("\nDone!")
    
    # Show completion message
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    messagebox.showinfo(
        "Complete",
        f"Duplicate scan complete!\n\n"
        f"Duplicate groups found: {total_groups}\n"
        f"Total files in groups: {total_files}"
    )
    root.destroy()


if __name__ == "__main__":
    main()
