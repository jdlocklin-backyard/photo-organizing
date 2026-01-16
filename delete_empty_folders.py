"""
Delete Empty Folders Script
Scans a folder and its subfolders, deletes junk files, then deletes all empty folders.
"""

import os
import fnmatch
from tkinter import Tk, filedialog, messagebox


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


def find_junk_files(folder_path: str, excluded_folder: str | None = None) -> list[str]:
    """Find all junk files matching specified patterns."""
    junk_patterns = ['.Bridge*', '.picas*', '.bak*']
    junk_files = []
    
    # Normalize excluded path for comparison
    excluded_normalized = None
    if excluded_folder:
        excluded_normalized = os.path.normpath(os.path.abspath(excluded_folder)).lower()
    
    for root, dirs, files in os.walk(folder_path):
        # Skip excluded folder
        if excluded_normalized:
            root_normalized = os.path.normpath(os.path.abspath(root)).lower()
            if root_normalized == excluded_normalized or root_normalized.startswith(excluded_normalized + os.sep):
                continue
        
        for filename in files:
            for pattern in junk_patterns:
                if fnmatch.fnmatch(filename.lower(), pattern.lower()):
                    junk_files.append(os.path.join(root, filename))
                    break
    
    return junk_files


def delete_junk_files(folder_path: str, excluded_folder: str | None = None) -> dict:
    """
    Delete all junk files matching specified patterns.
    
    Returns:
        Dictionary with statistics about the operation
    """
    stats = {
        "deleted": 0,
        "errors": []
    }
    
    junk_files = find_junk_files(folder_path, excluded_folder)
    
    for file_path in junk_files:
        try:
            os.remove(file_path)
            stats["deleted"] += 1
            print(f"Deleted file: {file_path}")
        except Exception as e:
            stats["errors"].append(f"{file_path}: {str(e)}")
            print(f"Error deleting {file_path}: {e}")
    
    return stats


def find_empty_folders(folder_path: str, excluded_folder: str | None = None) -> list[str]:
    """Find all empty folders in the given path, deepest first."""
    empty_folders = []
    
    # Normalize excluded path for comparison
    excluded_normalized = None
    if excluded_folder:
        excluded_normalized = os.path.normpath(os.path.abspath(excluded_folder)).lower()
    
    # Walk bottom-up so we can detect folders that become empty after subfolders are removed
    for root, dirs, files in os.walk(folder_path, topdown=False):
        # Skip excluded folder
        if excluded_normalized:
            root_normalized = os.path.normpath(os.path.abspath(root)).lower()
            if root_normalized == excluded_normalized or root_normalized.startswith(excluded_normalized + os.sep):
                continue
        
        # Check if directory is empty (no files and no subdirectories)
        if not dirs and not files:
            empty_folders.append(root)
    
    return empty_folders


def delete_empty_folders(folder_path: str, excluded_folder: str | None = None) -> dict:
    """
    Delete all empty folders in the given path.
    
    Returns:
        Dictionary with statistics about the operation
    """
    stats = {
        "deleted": 0,
        "errors": []
    }
    
    # Keep deleting until no more empty folders are found
    # This handles nested empty folders
    while True:
        empty_folders = find_empty_folders(folder_path, excluded_folder)
        
        if not empty_folders:
            break
        
        for folder in empty_folders:
            try:
                os.rmdir(folder)
                stats["deleted"] += 1
                print(f"Deleted: {folder}")
            except Exception as e:
                stats["errors"].append(f"{folder}: {str(e)}")
                print(f"Error deleting {folder}: {e}")
    
    return stats


def main():
    """Main function to run the empty folder cleaner."""
    print("=" * 60)
    print("     CLEANUP: JUNK FILES & EMPTY FOLDERS")
    print("=" * 60)
    print("\nThis script will:")
    print("  1. Delete junk files (.Bridge*, .picas*, .bak*)")
    print("  2. Delete all empty folders\n")
    
    # Select folder to scan
    print("Please select the folder to scan...")
    folder_path = select_folder("Select folder to scan")
    
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
    
    # --- PHASE 1: Delete junk files ---
    print("\n" + "-" * 60)
    print("PHASE 1: Scanning for junk files...")
    print("-" * 60)
    
    junk_files = find_junk_files(folder_path, excluded_folder)
    
    if junk_files:
        print(f"\nFound {len(junk_files)} junk file(s):")
        for f in junk_files[:20]:
            print(f"  - {f}")
        if len(junk_files) > 20:
            print(f"  ... and {len(junk_files) - 20} more")
        
        # Confirm junk file deletion
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_list = "\n".join([f"  • {os.path.basename(f)}" for f in junk_files[:10]])
        if len(junk_files) > 10:
            file_list += f"\n  ... and {len(junk_files) - 10} more"
        
        delete_junk = messagebox.askyesno(
            "Delete Junk Files",
            f"Found {len(junk_files)} junk file(s):\n\n"
            f"{file_list}\n\n"
            "Delete these files?"
        )
        root.destroy()
        
        if delete_junk:
            junk_stats = delete_junk_files(folder_path, excluded_folder)
            print(f"\nDeleted {junk_stats['deleted']} junk file(s)")
        else:
            print("\nSkipped junk file deletion.")
    else:
        print("\nNo junk files found.")
    
    # --- PHASE 2: Delete empty folders ---
    print("\n" + "-" * 60)
    print("PHASE 2: Scanning for empty folders...")
    print("-" * 60)
    
    # Find empty folders
    empty_folders = find_empty_folders(folder_path, excluded_folder)
    
    if not empty_folders:
        print("\nNo empty folders found!")
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showinfo("Complete", "Cleanup complete!\n\nNo empty folders found.")
        root.destroy()
        return
    
    # Show confirmation with list of folders to delete
    print(f"\nFound {len(empty_folders)} empty folder(s):")
    for folder in empty_folders[:20]:  # Show first 20
        print(f"  - {folder}")
    if len(empty_folders) > 20:
        print(f"  ... and {len(empty_folders) - 20} more")
    
    # Confirm before deleting
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    folder_list = "\n".join([f"  • {f}" for f in empty_folders[:10]])
    if len(empty_folders) > 10:
        folder_list += f"\n  ... and {len(empty_folders) - 10} more"
    
    proceed = messagebox.askyesno(
        "Confirm Delete",
        f"Found {len(empty_folders)} empty folder(s):\n\n"
        f"{folder_list}\n\n"
        "Delete all empty folders?"
    )
    root.destroy()
    
    if not proceed:
        print("Operation cancelled by user.")
        return
    
    print("\n" + "-" * 60)
    print("Deleting empty folders...")
    print("-" * 60 + "\n")
    
    # Delete empty folders
    stats = delete_empty_folders(folder_path, excluded_folder)
    
    # Print summary
    print("\n" + "=" * 60)
    print("                  SUMMARY")
    print("=" * 60)
    print(f"Folders deleted: {stats['deleted']}")
    
    if stats['errors']:
        print(f"Errors: {len(stats['errors'])}")
        for error in stats['errors'][:5]:
            print(f"  - {error}")
    
    print("\nDone!")
    
    # Show completion message
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    messagebox.showinfo(
        "Complete",
        f"Empty folder cleanup complete!\n\n"
        f"Folders deleted: {stats['deleted']}\n"
        f"Errors: {len(stats['errors'])}"
    )
    root.destroy()


if __name__ == "__main__":
    main()
