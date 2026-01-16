"""
Photo Organizer Script
Organizes photos into YYYY/YYYYMMDD/EXT folder structure based on creation date.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from tkinter import Tk, filedialog, messagebox
from PIL import Image
from PIL.ExifTags import TAGS


def get_exif_date(image_path: str) -> datetime | None:
    """Extract the 'Date Taken' (DateTimeOriginal) from image EXIF data."""
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                date_taken = None
                date_digitized = None
                
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    # DateTimeOriginal is the "Date Taken" field
                    if tag == "DateTimeOriginal":
                        date_taken = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    # DateTimeDigitized as fallback
                    elif tag == "DateTimeDigitized":
                        date_digitized = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                
                # Prioritize Date Taken over Date Digitized
                if date_taken:
                    return date_taken
                if date_digitized:
                    return date_digitized
    except Exception:
        pass
    return None


def get_file_creation_date(file_path: str) -> datetime:
    """Get file creation date (Windows) or metadata change time (Unix)."""
    stat = os.stat(file_path)
    # On Windows, st_ctime is the creation time
    # On Unix, st_ctime is the last metadata change time
    if os.name == 'nt':  # Windows
        creation_time = stat.st_ctime
    else:
        # On Unix, try to get birth time if available, otherwise use ctime
        try:
            creation_time = stat.st_birthtime
        except AttributeError:
            creation_time = stat.st_ctime
    return datetime.fromtimestamp(creation_time)


def find_matching_raw_file(image_path: str) -> str | None:
    """
    Find a corresponding RAW file (.nef, .arw, .dng, .raf) for a given image.
    Looks for files with the same base name in the same directory.
    """
    raw_extensions = ['.nef', '.arw', '.dng', '.raf']
    image_dir = Path(image_path).parent
    base_name = Path(image_path).stem
    
    for raw_ext in raw_extensions:
        # Check both lowercase and uppercase extensions
        for ext in [raw_ext, raw_ext.upper()]:
            raw_path = image_dir / f"{base_name}{ext}"
            if raw_path.exists():
                return str(raw_path)
    
    return None


def get_photo_date(image_path: str) -> datetime:
    """
    Get the date for organizing the photo.
    For JPG, CR2, PNG, XMP: Uses date from corresponding RAW file (.nef, .arw, .dng) if found
    For RAW formats: EXIF DateTimeOriginal > EXIF DateTimeDigitized > File Creation Date
    """
    ext = Path(image_path).suffix.lower()
    
    # For JPG, CR2, PNG, XMP files - try to find matching RAW file and use its date
    if ext in {'.jpg', '.jpeg', '.cr2', '.png', '.xmp'}:
        raw_file = find_matching_raw_file(image_path)
        if raw_file:
            # Use the RAW file's date
            exif_date = get_exif_date(raw_file)
            if exif_date:
                return exif_date
            return get_file_creation_date(raw_file)
        # No matching RAW file found, use own creation date
        return get_file_creation_date(image_path)
    
    # For RAW formats, try EXIF data first
    exif_date = get_exif_date(image_path)
    if exif_date:
        return exif_date
    
    # Fall back to file creation date
    return get_file_creation_date(image_path)


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


def select_folder(title: str = "Select Folder") -> str | None:
    """Open a folder selection dialog and return the selected path."""
    root = Tk()
    root.withdraw()  # Hide the main window
    root.attributes('-topmost', True)  # Bring dialog to front
    root.focus_force()  # Force focus to ensure dialog appears
    root.update()  # Process pending events
    
    folder_path = filedialog.askdirectory(title=title, parent=root)
    root.destroy()
    
    return folder_path if folder_path else None


def organize_photos(source_folder: str, destination_folder: str | None = None, 
                    copy_files: bool = True) -> dict:
    """
    Organize photos from source folder into YYYY/YYYYMMDD/EXT structure.
    
    Args:
        source_folder: Path to scan for photos
        destination_folder: Where to save organized photos (defaults to source_folder/Organized)
        copy_files: If True, copy files; if False, move files
    
    Returns:
        Dictionary with statistics about the operation
    """
    if destination_folder is None:
        destination_folder = os.path.join(source_folder, "Organized")
    
    stats = {
        "total_found": 0,
        "organized": 0,
        "skipped": 0,
        "errors": []
    }
    
    # Normalize destination path for comparison
    dest_normalized = os.path.normpath(os.path.abspath(destination_folder)).lower()
    
    # Walk through all directories
    for root, dirs, files in os.walk(source_folder):
        # Skip the destination folder to avoid processing already organized files
        root_normalized = os.path.normpath(os.path.abspath(root)).lower()
        if root_normalized == dest_normalized or root_normalized.startswith(dest_normalized + os.sep):
            continue
            
        for filename in files:
            file_path = os.path.join(root, filename)
            
            if not is_image_file(file_path):
                continue
            
            stats["total_found"] += 1
            
            try:
                # Get the photo date
                photo_date = get_photo_date(file_path)
                
                # Get file extension (uppercase, without dot)
                file_ext = Path(file_path).suffix.upper().lstrip('.')
                
                # Create folder structure: YYYY/YYYYMMDD/EXT
                year_folder = photo_date.strftime("%Y")
                day_folder = photo_date.strftime("%Y%m%d")
                
                target_dir = os.path.join(destination_folder, year_folder, day_folder, file_ext)
                os.makedirs(target_dir, exist_ok=True)
                
                # Handle duplicate filenames
                target_path = os.path.join(target_dir, filename)
                if os.path.exists(target_path):
                    # Add a number suffix to avoid overwriting
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(target_path):
                        new_filename = f"{base}_{counter}{ext}"
                        target_path = os.path.join(target_dir, new_filename)
                        counter += 1
                
                # Copy or move the file
                if copy_files:
                    shutil.copy2(file_path, target_path)
                else:
                    shutil.move(file_path, target_path)
                
                stats["organized"] += 1
                print(f"{'Copied' if copy_files else 'Moved'}: {filename} -> {target_path}")
                
            except Exception as e:
                stats["skipped"] += 1
                stats["errors"].append(f"{file_path}: {str(e)}")
                print(f"Error processing {filename}: {e}")
    
    return stats


def main():
    """Main function to run the photo organizer."""
    print("=" * 60)
    print("           PHOTO ORGANIZER")
    print("=" * 60)
    print("\nThis script will organize your photos into folders")
    print("based on their creation date (YYYY/YYYYMMDD/EXT).\n")
    
    # Select source folder
    print("Please select the folder containing photos to organize...")
    source_folder = select_folder("Select folder with photos to organize")
    
    if not source_folder:
        print("No folder selected. Exiting.")
        return
    
    print(f"\nSource folder: {source_folder}")
    
    # Ask user if they want to specify a destination folder
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    use_custom_dest = messagebox.askyesno(
        "Destination Folder",
        "Do you want to specify a custom destination folder?\n\n"
        "Click 'No' to create an 'Organized' folder in the source location."
    )
    root.destroy()
    
    destination_folder = None
    if use_custom_dest:
        print("Please select the destination folder...")
        destination_folder = select_folder("Select destination folder")
        if destination_folder:
            print(f"Destination folder: {destination_folder}")
    
    if destination_folder is None:
        destination_folder = os.path.join(source_folder, "Organized")
        print(f"Destination folder: {destination_folder}")
    
    # Ask user if they want to copy or move files
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    copy_files = messagebox.askyesno(
        "Copy or Move",
        "Do you want to COPY the files?\n\n"
        "Click 'Yes' to copy (keeps originals)\n"
        "Click 'No' to move (removes originals)"
    )
    root.destroy()
    
    action = "copy" if copy_files else "move"
    print(f"\nAction: {action.upper()} files")
    
    # Confirm before proceeding
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    # Determine excluded folders
    excluded_folders = [destination_folder]
    excluded_text = "\n".join([f"  • {folder}" for folder in excluded_folders])
    
    proceed = messagebox.askyesno(
        "Confirm",
        f"Ready to {action} photos?\n\n"
        f"Source: {source_folder}\n"
        f"Destination: {destination_folder}\n\n"
        f"Excluded folders:\n{excluded_text}\n\n"
        "Click 'Yes' to proceed."
    )
    root.destroy()
    
    if not proceed:
        print("Operation cancelled by user.")
        return
    
    print("\n" + "-" * 60)
    print("Processing photos...")
    print("-" * 60 + "\n")
    
    # Run the organizer
    stats = organize_photos(source_folder, destination_folder, copy_files)
    
    # Print summary
    print("\n" + "=" * 60)
    print("                  SUMMARY")
    print("=" * 60)
    print(f"Total photos found: {stats['total_found']}")
    print(f"Successfully organized: {stats['organized']}")
    print(f"Skipped/Errors: {stats['skipped']}")
    
    if stats['errors']:
        print("\nErrors encountered:")
        for error in stats['errors'][:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(stats['errors']) > 10:
            print(f"  ... and {len(stats['errors']) - 10} more errors")
    
    print("\nDone!")
    
    # Show completion message
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    messagebox.showinfo(
        "Complete",
        f"Photo organization complete!\n\n"
        f"Total photos found: {stats['total_found']}\n"
        f"Successfully organized: {stats['organized']}\n"
        f"Skipped/Errors: {stats['skipped']}"
    )
    root.destroy()


if __name__ == "__main__":
    main()
