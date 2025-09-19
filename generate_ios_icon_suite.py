#!/usr/bin/env python3
"""
Generate complete iOS icon suite from appicon.png
Creates all required icon sizes for iOS apps according to Apple's guidelines.
"""

from PIL import Image
import os

def generate_ios_icon_suite(source_image_path, output_dir="AppIcon.appiconset"):
    """
    Generate complete iOS icon suite from source image.
    
    Args:
        source_image_path: Path to the source 1024x1024 icon image
        output_dir: Directory to save the icon suite
    """
    
    # iOS Icon sizes (in pixels) - covers all device types and contexts
    icon_sizes = {
        # iPhone App Icons
        "Icon-App-20x20@1x.png": 20,
        "Icon-App-20x20@2x.png": 40,
        "Icon-App-20x20@3x.png": 60,
        "Icon-App-29x29@1x.png": 29,
        "Icon-App-29x29@2x.png": 58,
        "Icon-App-29x29@3x.png": 87,
        "Icon-App-40x40@1x.png": 40,
        "Icon-App-40x40@2x.png": 80,
        "Icon-App-40x40@3x.png": 120,
        "Icon-App-60x60@2x.png": 120,
        "Icon-App-60x60@3x.png": 180,
        
        # iPad App Icons
        "Icon-App-20x20@1x~ipad.png": 20,
        "Icon-App-20x20@2x~ipad.png": 40,
        "Icon-App-29x29@1x~ipad.png": 29,
        "Icon-App-29x29@2x~ipad.png": 58,
        "Icon-App-40x40@1x~ipad.png": 40,
        "Icon-App-40x40@2x~ipad.png": 80,
        "Icon-App-76x76@1x~ipad.png": 76,
        "Icon-App-76x76@2x~ipad.png": 152,
        "Icon-App-83.5x83.5@2x~ipad.png": 167,
        
        # App Store
        "ItunesArtwork@2x.png": 1024,
        
        # Common additional sizes
        "Icon-16.png": 16,
        "Icon-32.png": 32,
        "Icon-64.png": 64,
        "Icon-128.png": 128,
        "Icon-256.png": 256,
        "Icon-512.png": 512,
        "Icon-1024.png": 1024,
    }
    
    try:
        # Load source image
        print(f"Loading source image: {source_image_path}")
        source_img = Image.open(source_image_path)
        
        # Verify source image is square
        if source_img.size[0] != source_img.size[1]:
            raise ValueError(f"Source image must be square. Current size: {source_img.size}")
        
        print(f"Source image size: {source_img.size[0]}x{source_img.size[1]}")
        
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        
        generated_count = 0
        
        # Generate all icon sizes
        for filename, size in icon_sizes.items():
            try:
                # Resize image using high-quality resampling
                resized_img = source_img.resize((size, size), Image.Resampling.LANCZOS)
                
                # Save the resized icon
                output_path = os.path.join(output_dir, filename)
                resized_img.save(output_path, 'PNG', optimize=True, quality=100)
                
                print(f"✓ Generated: {filename} ({size}x{size})")
                generated_count += 1
                
            except Exception as e:
                print(f"✗ Error generating {filename}: {e}")
        
        # Generate Contents.json for Xcode
        contents_json = generate_contents_json()
        contents_path = os.path.join(output_dir, "Contents.json")
        
        with open(contents_path, 'w') as f:
            f.write(contents_json)
        
        print(f"\n✓ Generated Contents.json for Xcode integration")
        print(f"\n🎉 Successfully generated {generated_count} icon files!")
        print(f"📁 All icons saved in: {output_dir}")
        print(f"\n📱 Your iOS icon suite is ready for Xcode!")
        print(f"   Simply drag the '{output_dir}' folder into your Xcode project's")
        print(f"   App Icons & Launch Images section.")
        
    except FileNotFoundError:
        print(f"❌ Error: Source image '{source_image_path}' not found!")
    except Exception as e:
        print(f"❌ Error: {e}")

def generate_contents_json():
    """Generate Contents.json file for Xcode AppIcon.appiconset"""
    return '''{
  "images" : [
    {
      "filename" : "Icon-App-20x20@2x.png",
      "idiom" : "iphone",
      "scale" : "2x",
      "size" : "20x20"
    },
    {
      "filename" : "Icon-App-20x20@3x.png",
      "idiom" : "iphone",
      "scale" : "3x",
      "size" : "20x20"
    },
    {
      "filename" : "Icon-App-29x29@2x.png",
      "idiom" : "iphone",
      "scale" : "2x",
      "size" : "29x29"
    },
    {
      "filename" : "Icon-App-29x29@3x.png",
      "idiom" : "iphone",
      "scale" : "3x",
      "size" : "29x29"
    },
    {
      "filename" : "Icon-App-40x40@2x.png",
      "idiom" : "iphone",
      "scale" : "2x",
      "size" : "40x40"
    },
    {
      "filename" : "Icon-App-40x40@3x.png",
      "idiom" : "iphone",
      "scale" : "3x",
      "size" : "40x40"
    },
    {
      "filename" : "Icon-App-60x60@2x.png",
      "idiom" : "iphone",
      "scale" : "2x",
      "size" : "60x60"
    },
    {
      "filename" : "Icon-App-60x60@3x.png",
      "idiom" : "iphone",
      "scale" : "3x",
      "size" : "60x60"
    },
    {
      "filename" : "Icon-App-20x20@1x~ipad.png",
      "idiom" : "ipad",
      "scale" : "1x",
      "size" : "20x20"
    },
    {
      "filename" : "Icon-App-20x20@2x~ipad.png",
      "idiom" : "ipad",
      "scale" : "2x",
      "size" : "20x20"
    },
    {
      "filename" : "Icon-App-29x29@1x~ipad.png",
      "idiom" : "ipad",
      "scale" : "1x",
      "size" : "29x29"
    },
    {
      "filename" : "Icon-App-29x29@2x~ipad.png",
      "idiom" : "ipad",
      "scale" : "2x",
      "size" : "29x29"
    },
    {
      "filename" : "Icon-App-40x40@1x~ipad.png",
      "idiom" : "ipad",
      "scale" : "1x",
      "size" : "40x40"
    },
    {
      "filename" : "Icon-App-40x40@2x~ipad.png",
      "idiom" : "ipad",
      "scale" : "2x",
      "size" : "40x40"
    },
    {
      "filename" : "Icon-App-76x76@1x~ipad.png",
      "idiom" : "ipad",
      "scale" : "1x",
      "size" : "76x76"
    },
    {
      "filename" : "Icon-App-76x76@2x~ipad.png",
      "idiom" : "ipad",
      "scale" : "2x",
      "size" : "76x76"
    },
    {
      "filename" : "Icon-App-83.5x83.5@2x~ipad.png",
      "idiom" : "ipad",
      "scale" : "2x",
      "size" : "83.5x83.5"
    },
    {
      "filename" : "ItunesArtwork@2x.png",
      "idiom" : "ios-marketing",
      "scale" : "1x",
      "size" : "1024x1024"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}'''

def main():
    """Main function to generate iOS icon suite."""
    source_file = "appicon.png"
    
    if not os.path.exists(source_file):
        print(f"❌ Error: {source_file} not found in current directory!")
        print("Please make sure appicon.png exists and is a 1024x1024 square image.")
        return
    
    print("🚀 Generating iOS Icon Suite from appicon.png")
    print("=" * 50)
    
    generate_ios_icon_suite(source_file)

if __name__ == "__main__":
    main()
