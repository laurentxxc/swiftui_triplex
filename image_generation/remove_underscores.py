#!/usr/bin/env python3
"""
Remove all underscore characters from filenames in generated_images directory.
"""

import os
import glob

def remove_underscores():
    """Remove all underscore characters from PNG filenames."""
    
    # Get all PNG files in generated_images directory
    image_dir = 'generated_images'
    if not os.path.exists(image_dir):
        print(f"Directory {image_dir} does not exist!")
        return
    
    png_files = glob.glob(os.path.join(image_dir, '*.png'))
    
    if not png_files:
        print(f"No PNG files found in {image_dir}")
        return
    
    print(f"Found {len(png_files)} files to rename...")
    
    renamed_count = 0
    
    for old_filepath in png_files:
        # Get just the filename without path
        old_filename = os.path.basename(old_filepath)
        
        # Remove all underscores from filename
        new_filename = old_filename.replace('_', '')
        
        # Create new filepath
        new_filepath = os.path.join(image_dir, new_filename)
        
        # Rename the file
        if old_filepath != new_filepath:
            try:
                os.rename(old_filepath, new_filepath)
                print(f"Renamed: {old_filename} -> {new_filename}")
                renamed_count += 1
            except OSError as e:
                print(f"Error renaming {old_filename}: {e}")
        else:
            print(f"No change needed for: {old_filename}")
    
    print(f"\nSuccessfully renamed {renamed_count} files!")

if __name__ == "__main__":
    remove_underscores()
