#!/usr/bin/env python3
"""
Rename image files in generated_images directory according to mapping:
- ball, red, cloudy_sky -> 1
- bottle, blue, jungle -> 2  
- pen, green, desert -> 3
"""

import os
import glob

def rename_files():
    """Rename all PNG files in generated_images directory."""
    
    # Mapping dictionary
    replacements = {
        'ball': '1',
        'red': '1', 
        'cloudy_sky': '1',
        'bottle': '2',
        'blue': '2',
        'jungle': '2',
        'pen': '3',
        'green': '3',
        'desert': '3'
    }
    
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
        
        # Start with the original filename (without .png extension)
        new_filename = old_filename[:-4]  # Remove .png
        
        # Apply all replacements
        for old_term, new_term in replacements.items():
            new_filename = new_filename.replace(old_term, new_term)
        
        # Add .png extension back
        new_filename += '.png'
        
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
    rename_files()
