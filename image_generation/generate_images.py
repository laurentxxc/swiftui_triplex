#!/usr/bin/env python3
"""
Generate 81 PNG images with combinations of:
- 1, 2, or 3 items
- Item types: ball, bottle, pen
- Colors: red, blue, green
- Backgrounds: cloudy sky, jungle, desert
"""

from PIL import Image, ImageDraw
import os
import math

# Image dimensions
WIDTH = 500
HEIGHT = 500

# Color definitions
COLORS = {
    'red': '#FF0000',
    'blue': '#0000FF',
    'green': "#F0EB46"
}

# Background colors
BACKGROUNDS = {
    'cloudy_sky': '#87CEEB',  # Sky blue
    'jungle': "#7FB97F",     # Forest green
    'desert': '#F4A460'      # Sandy brown
}

def create_background(bg_type):
    """Create a background pattern based on type."""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    
    if bg_type == 'cloudy_sky':
        # Sky blue base with white clouds
        img.paste(BACKGROUNDS['cloudy_sky'], (0, 0, WIDTH, HEIGHT))
        # Add some cloud-like white patches
        for i in range(8):
            x = (i % 3) * 150 + 50
            y = (i // 3) * 120 + 30
            draw.ellipse([x, y, x + 80, y + 40], fill='#FFFFFF', outline=None)
            draw.ellipse([x + 30, y - 10, x + 110, y + 30], fill='#FFFFFF', outline=None)
    
    elif bg_type == 'jungle':
        # Forest green base with darker green patches
        img.paste(BACKGROUNDS['jungle'], (0, 0, WIDTH, HEIGHT))
        # Add tree-like patterns
        for i in range(12):
            x = (i % 4) * 125 + 25
            y = (i // 4) * 150 + 25
            draw.ellipse([x, y, x + 60, y + 80], fill='#006400', outline=None)
            draw.ellipse([x + 20, y + 10, x + 80, y + 90], fill='#004000', outline=None)
    
    elif bg_type == 'desert':
        # Sandy brown base with dune patterns
        img.paste(BACKGROUNDS['desert'], (0, 0, WIDTH, HEIGHT))
        # Add sand dune curves
        for i in range(6):
            y = i * 80 + 40
            for x in range(0, WIDTH, 50):
                wave_y = y + int(20 * math.sin(x / 50))
                draw.ellipse([x, wave_y, x + 40, wave_y + 20], fill='#D2691E', outline=None)
    
    return img

def draw_ball(draw, x, y, size, color):
    """Draw a ball (circle) at given position."""
    radius = size // 2
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], 
                fill=color, outline='#000000', width=2)
    # Add highlight
    highlight_x = x - radius // 3
    highlight_y = y - radius // 3
    highlight_radius = radius // 4
    draw.ellipse([highlight_x - highlight_radius, highlight_y - highlight_radius,
                 highlight_x + highlight_radius, highlight_y + highlight_radius],
                fill='#FFFFFF', outline=None)

def draw_bottle(draw, x, y, size, color):
    """Draw a bottle at given position."""
    width = size // 2
    height = int(size * 1.2)
    neck_width = width // 3
    neck_height = height // 4
    
    # Main body
    draw.rectangle([x - width//2, y - height//2, x + width//2, y + height//2],
                  fill=color, outline='#000000', width=2)
    # Neck
    draw.rectangle([x - neck_width//2, y - height//2 - neck_height, 
                   x + neck_width//2, y - height//2],
                  fill=color, outline='#000000', width=2)
    # Cap
    cap_width = int(neck_width * 1.2)
    draw.rectangle([x - cap_width//2, y - height//2 - neck_height - 10,
                   x + cap_width//2, y - height//2 - neck_height],
                  fill='#333333', outline='#000000', width=1)

def draw_pen(draw, x, y, size, color):
    """Draw a pen at given position, rotated 45 degrees."""

    width = size // 5
    length = int(size * 1.1)
    angle = math.radians(45)

    # Helper to rotate a point around (x, y)
    def rotate(px, py):
        dx, dy = px - x, py - y
        rx = dx * math.cos(angle) - dy * math.sin(angle) + x
        ry = dx * math.sin(angle) + dy * math.cos(angle) + y
        return (rx, ry)

    # Main body rectangle corners
    body = [
        (x - length//2, y - width//2),
        (x + length//2, y - width//2),
        (x + length//2, y + width//2),
        (x - length//2, y + width//2)
    ]
    body_rot = [rotate(px, py) for px, py in body]
    draw.polygon(body_rot, fill=color, outline='#000000')

    # Tip polygon
    tip_size = width
    tip = [
        (x + length//2, y - tip_size//2),
        (x + length//2, y + tip_size//2),
        (x + length//2 + tip_size, y)
    ]
    tip_rot = [rotate(px, py) for px, py in tip]
    draw.polygon(tip_rot, fill='#333333', outline='#000000')

    # Clip rectangle corners
    clip_width = width//2
    clip_length = width
    clip = [
        (x - length//2 - clip_width, y - clip_length//2),
        (x - length//2, y - clip_length//2),
        (x - length//2, y + clip_length//2),
        (x - length//2 - clip_width, y + clip_length//2)
    ]
    clip_rot = [rotate(px, py) for px, py in clip]
    draw.polygon(clip_rot, fill='#666666', outline='#000000')

def generate_image(num_items, item_type, color, background):
    """Generate a single image with specified parameters."""
    # Create background
    img = create_background(background)
    draw = ImageDraw.Draw(img)
    
    # Item size
    base_size = 120
    
    # Position items based on count
    positions = []
    if num_items == 1:
        positions = [(WIDTH//2, HEIGHT//2)]
    elif num_items == 2:
        positions = [(WIDTH//3, HEIGHT//2), (2*WIDTH//3, HEIGHT//2)]
    else:  # num_items == 3
        positions = [(WIDTH//4, HEIGHT//2), (WIDTH//2, HEIGHT//2), (3*WIDTH//4, HEIGHT//2)]
    
    # Draw items
    for pos in positions:
        x, y = pos
        if item_type == 'ball':
            draw_ball(draw, x, y, base_size, COLORS[color])
        elif item_type == 'bottle':
            draw_bottle(draw, x, y, base_size, COLORS[color])
        elif item_type == 'pen':
            draw_pen(draw, x, y, base_size, COLORS[color])
    
    return img

def main():
    """Generate all 81 image combinations."""
    # Create output directory
    output_dir = "generated_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    count = 0
    
    # Generate all combinations
    for num_items in [1, 2, 3]:
        for item_type in ['ball', 'bottle', 'pen']:
            for color in ['red', 'blue', 'green']:
                for background in ['cloudy_sky', 'jungle', 'desert']:
                    count += 1
                    print(f"Generating image {count}/81: {num_items} {color} {item_type}(s) on {background}")
                    
                    # Generate image
                    img = generate_image(num_items, item_type, color, background)
                    
                    # Save image
                    filename = f"{num_items}_{item_type}_{color}_{background}.png"
                    filepath = os.path.join(output_dir, filename)
                    img.save(filepath, 'PNG')
    
    print(f"Successfully generated {count} images in '{output_dir}' directory!")

if __name__ == "__main__":
    main()
