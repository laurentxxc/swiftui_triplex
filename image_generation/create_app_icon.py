#!/usr/bin/env python3
"""
Create a 1024x1024 app icon for Triplex iOS game.
The icon will showcase the game's core concept with multiple colorful items
arranged in an appealing composition with a gradient background.
"""

from PIL import Image, ImageDraw, ImageFilter
import math

# Icon dimensions
ICON_SIZE = 1024
CENTER_X = ICON_SIZE // 2
CENTER_Y = ICON_SIZE // 2

# Colors
COLORS = {
    'red': '#FF3B30',      # iOS red
    'blue': '#007AFF',     # iOS blue  
    'green': '#34C759'     # iOS green
}

# Background gradient colors
BG_TOP = '#FF6B6B'      # Coral red
BG_BOTTOM = '#4ECDC4'   # Turquoise

def create_gradient_background():
    """Create a radial gradient background."""
    img = Image.new('RGB', (ICON_SIZE, ICON_SIZE))
    draw = ImageDraw.Draw(img)
    
    # Create radial gradient from center
    for radius in range(0, int(ICON_SIZE * 0.8), 2):
        # Interpolate between colors based on radius
        progress = radius / (ICON_SIZE * 0.8)
        
        # RGB interpolation
        r1, g1, b1 = int(BG_TOP[1:3], 16), int(BG_TOP[3:5], 16), int(BG_TOP[5:7], 16)
        r2, g2, b2 = int(BG_BOTTOM[1:3], 16), int(BG_BOTTOM[3:5], 16), int(BG_BOTTOM[5:7], 16)
        
        r = int(r1 + (r2 - r1) * progress)
        g = int(g1 + (g2 - g1) * progress)  
        b = int(b1 + (b2 - b1) * progress)
        
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        draw.ellipse([CENTER_X - radius, CENTER_Y - radius, 
                     CENTER_X + radius, CENTER_Y + radius], 
                    outline=color, width=2)
    
    return img

def draw_ball(draw, x, y, size, color, shadow=True):
    """Draw a stylized ball with shadow and highlight."""
    radius = size // 2
    
    # Shadow (slightly offset)
    if shadow:
        shadow_offset = size // 20
        draw.ellipse([x - radius + shadow_offset, y - radius + shadow_offset, 
                     x + radius + shadow_offset, y + radius + shadow_offset], 
                    fill='#00000030', outline=None)
    
    # Main ball
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], 
                fill=color, outline='#FFFFFF', width=size//25)
    
    # Highlight
    highlight_x = x - radius // 3
    highlight_y = y - radius // 3
    highlight_radius = radius // 3
    draw.ellipse([highlight_x - highlight_radius, highlight_y - highlight_radius,
                 highlight_x + highlight_radius, highlight_y + highlight_radius],
                fill='#FFFFFF80', outline=None)

def draw_bottle(draw, x, y, size, color, shadow=True):
    """Draw a stylized bottle with shadow."""
    width = size // 2
    height = int(size * 1.2)
    neck_width = width // 3
    neck_height = height // 4
    
    # Shadow
    if shadow:
        shadow_offset = size // 20
        draw.rectangle([x - width//2 + shadow_offset, y - height//2 + shadow_offset, 
                       x + width//2 + shadow_offset, y + height//2 + shadow_offset],
                      fill='#00000030', outline=None)
    
    # Main body
    draw.rectangle([x - width//2, y - height//2, x + width//2, y + height//2],
                  fill=color, outline='#FFFFFF', width=size//25)
    
    # Neck
    draw.rectangle([x - neck_width//2, y - height//2 - neck_height, 
                   x + neck_width//2, y - height//2],
                  fill=color, outline='#FFFFFF', width=size//30)
    
    # Cap
    cap_width = int(neck_width * 1.2)
    draw.rectangle([x - cap_width//2, y - height//2 - neck_height - size//15,
                   x + cap_width//2, y - height//2 - neck_height],
                  fill='#333333', outline='#FFFFFF', width=1)

def draw_pen(draw, x, y, size, color, shadow=True):
    """Draw a stylized pen with shadow."""
    width = size // 8
    length = int(size * 1.1)
    
    # Shadow
    if shadow:
        shadow_offset = size // 20
        draw.rectangle([x - length//2 + shadow_offset, y - width//2 + shadow_offset, 
                       x + length//2 + shadow_offset, y + width//2 + shadow_offset],
                      fill='#00000030', outline=None)
    
    # Main body
    draw.rectangle([x - length//2, y - width//2, x + length//2, y + width//2],
                  fill=color, outline='#FFFFFF', width=size//40)
    
    # Tip
    tip_size = width + 4
    draw.polygon([x + length//2, y - tip_size//2,
                 x + length//2, y + tip_size//2,
                 x + length//2 + tip_size, y],
                fill='#333333', outline='#FFFFFF')
    
    # Clip
    clip_width = width // 2
    clip_length = length // 4
    draw.rectangle([x - length//2 - clip_width, y - clip_length//2,
                   x - length//2, y + clip_length//2],
                  fill='#666666', outline='#FFFFFF', width=1)

def create_app_icon():
    """Create the main app icon."""
    # Create gradient background
    img = create_gradient_background()
    draw = ImageDraw.Draw(img)
    
    # Add subtle corner rounding effect (iOS style)
    corner_radius = ICON_SIZE // 8
    mask = Image.new('L', (ICON_SIZE, ICON_SIZE), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, ICON_SIZE, ICON_SIZE], 
                               radius=corner_radius, fill=255)
    
    # Create the main composition - arrange items in a triangular pattern
    item_size = ICON_SIZE // 6
    
    # Top item (ball)
    top_x = CENTER_X
    top_y = CENTER_Y - ICON_SIZE // 4
    draw_ball(draw, top_x, top_y, item_size, COLORS['red'])
    
    # Bottom left item (bottle)
    bottom_left_x = CENTER_X - ICON_SIZE // 5
    bottom_left_y = CENTER_Y + ICON_SIZE // 6
    draw_bottle(draw, bottom_left_x, bottom_left_y, item_size, COLORS['blue'])
    
    # Bottom right item (pen)
    bottom_right_x = CENTER_X + ICON_SIZE // 5
    bottom_right_y = CENTER_Y + ICON_SIZE // 6
    draw_pen(draw, bottom_right_x, bottom_right_y, item_size, COLORS['green'])
    
    # Add title text area with subtle background
    text_bg_y = CENTER_Y + ICON_SIZE // 3
    text_bg_height = ICON_SIZE // 8
    draw.rectangle([ICON_SIZE // 8, text_bg_y, 
                   ICON_SIZE - ICON_SIZE // 8, text_bg_y + text_bg_height],
                  fill='#FFFFFF40', outline=None)
    
    # Add connecting lines to suggest combination/matching gameplay
    line_width = 6
    line_color = '#FFFFFF60'
    
    # Lines connecting the three items
    draw.line([top_x, top_y + item_size//2, bottom_left_x, bottom_left_y - item_size//2], 
             fill=line_color, width=line_width)
    draw.line([top_x, top_y + item_size//2, bottom_right_x, bottom_right_y - item_size//2], 
             fill=line_color, width=line_width)
    draw.line([bottom_left_x + item_size//2, bottom_left_y, 
              bottom_right_x - item_size//2, bottom_right_y], 
             fill=line_color, width=line_width)
    
    # Apply corner radius mask
    img.putalpha(mask)
    
    # Convert back to RGB for final save
    final_img = Image.new('RGB', (ICON_SIZE, ICON_SIZE), 'white')
    final_img.paste(img, (0, 0), img)
    
    return final_img

def main():
    """Generate the app icon."""
    print("Creating Triplex app icon (1024x1024)...")
    
    icon = create_app_icon()
    
    # Save the icon
    icon_path = "triplex_app_icon_1024.png"
    icon.save(icon_path, 'PNG', quality=100)
    
    print(f"App icon saved as: {icon_path}")
    print("This icon is ready for iOS app submission!")
    
    # Also create some common iOS icon sizes
    sizes = [512, 256, 128, 64]
    for size in sizes:
        resized_icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        resized_path = f"triplex_app_icon_{size}.png"
        resized_icon.save(resized_path, 'PNG', quality=100)
        print(f"Created {size}x{size} version: {resized_path}")

if __name__ == "__main__":
    main()
