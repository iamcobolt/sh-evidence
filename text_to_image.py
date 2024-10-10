#!/usr/bin/env python3

"""
text_to_image.py

This script converts text from a log file into a styled image representation.
It is part of the sh-evidence utility, which captures shell command output
and generates screenshots.

The script uses the Pillow library for image manipulation and Pygments for
syntax highlighting. It reads the log file, applies styling and formatting,
and generates an image that resembles a terminal or code editor window.

Key features:
- Reads text from a log file
- Applies syntax highlighting
- Creates an image with customizable font, padding, and colors
- Adds a border to simulate a window appearance

Usage:
This script is typically called by the sh-evidence shell utility and is not
intended to be run directly by users.
"""

import sys
import os

# PIL (Python Imaging Library) imports for image processing
from PIL import Image  # For creating and manipulating images
from PIL import ImageDraw  # For drawing on images
from PIL import ImageFilter  # For applying filters to images
from PIL import ImageFont  # For loading and using fonts in images

# Pygments imports for syntax highlighting
from pygments import highlight  # Core function for syntax highlighting
from pygments.lexers import get_lexer_by_name  # For getting the appropriate lexer for syntax highlighting
from pygments.formatters.img import ImageFormatter  # For formatting highlighted code as an image
from pygments.styles import get_style_by_name  # For getting predefined syntax highlighting styles


def get_token_style(token):
    # Get the style for a given token using the 'monokai' style
    style = get_style_by_name("monokai")
    return style.style_for_token(token)

def read_log_file(log_file_path):
    # Read the contents of a log file
    with open(log_file_path, "r") as f:
        return f.read()

def get_font(font_size):
    # Get the font object for the specified font size
    # First try to find the font in the current directory, then in the support directory
    font_file = os.path.join(os.getcwd(), "DejaVuSansMono.ttf")
    try:
        return ImageFont.truetype(font_file, font_size)
    except OSError:
        font_file = os.path.join(os.getcwd(), "./support/DejaVuSansMono.ttf")
        return ImageFont.truetype(font_file, font_size)

def add_padding(text, padding):
    # Add padding to the text
    # padding is a tuple of (left, top, right, bottom) padding values
    text_lines = text.split("\n")
    max_width = max([len(line) for line in text_lines])
    text_lines_padded = []
    for line in text_lines:
        padding_left = " " * ((max_width - len(line)) // 2 + padding[0])
        padding_right = " " * ((max_width - len(line) + 1) // 2 + padding[2])
        padded_line = padding_left + line + padding_right
        text_lines_padded.append(padded_line)
    text_lines_padded.append(" " * padding[0])  # add a blank line for padding at the bottom
    return text_lines_padded

def get_image_size(font, text_lines_padded, padding):
    # Calculate the required image size based on the text and padding
    line_height = int(font.getbbox("A")[3])
    img_width = int(max(font.getbbox(line)[2] for line in text_lines_padded) + padding[0] + padding[2])
    img_height = int(line_height * len(text_lines_padded) + padding[0] + padding[3])
    return img_width, img_height

def create_image(highlighted_code, font, img_size, bg_color, text_color, padding):
    # Create an image with the highlighted code and window-like appearance
    border_width = 25
    border_color = (60, 60, 60)
    inner_rect_size = (img_size[0] - border_width * 2, img_size[1] - border_width * 2)
    inner_rect_pos = (border_width, border_width)
    
    # Create a new RGBA image with the given size and background color
    img = Image.new("RGBA", img_size, border_color)
    draw = ImageDraw.Draw(img)
    
    # Draw the inner rectangle with the given padding
    draw.rectangle((inner_rect_pos, tuple(map(sum, zip(inner_rect_pos, inner_rect_size)))), fill=bg_color)
    
    # Draw the top bar of the window
    bar_pos = (inner_rect_pos[0], inner_rect_pos[1] - 30)
    bar_size = (inner_rect_size[0], 30)
    draw.rectangle((bar_pos, tuple(map(sum, zip(bar_pos, bar_size)))), fill=(67, 73, 81))
    
    # Draw the title text on the top bar
    title_text = "Terminal"
    title_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
    title_text_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_text_pos = (bar_pos[0] + 10, bar_pos[1] + (bar_size[1] - title_text_bbox[1]) // 2)
    draw.text(title_text_pos, title_text, font=title_font, fill=(180, 180, 180))
    
    # Draw the window control buttons (minimize, resize, close)
    button_size = (20, 20)
    draw.ellipse((bar_pos[0] + bar_size[0] - 80, bar_pos[1] + 5, bar_pos[0] + bar_size[0] - 60, bar_pos[1] + 25), fill=(239, 184, 56))
    draw.ellipse((bar_pos[0] + bar_size[0] - 50, bar_pos[1] + 5, bar_pos[0] + bar_size[0] - 30, bar_pos[1] + 25), fill=(122, 189, 83))
    draw.ellipse((bar_pos[0] + bar_size[0] - 20, bar_pos[1] + 5, bar_pos[0] + bar_size[0], bar_pos[1] + 25), fill=(226, 56, 62))
    
    # Draw the highlighted text onto the image
    y_offset = title_text_pos[1] + title_text_bbox[3] + padding[1]
    draw_highlighted_text(highlighted_code, draw, font, text_color, (padding[0] + inner_rect_pos[0], y_offset))
    return img

def draw_highlighted_text(highlighted_text, draw, font, text_color, padding):
    # Draw the highlighted text onto the image
    x, y = padding
    for line in highlighted_text.splitlines():
        line_bbox = draw.textbbox((x, y), line, font=font, stroke_width=0)
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_bbox[3] - line_bbox[1] + 1

def save_image(image, output_file_path):
    # Save the image to a file
    image.save(output_file_path)

def drop_shadow(image, shadow_color=(0, 0, 0, 100), offset=(5, 5), blur_radius=10):
    # Add a drop shadow effect to the image
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle((offset[0], offset[1], image.size[0] + offset[0], image.size[1] + offset[1]), fill=shadow_color)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    # Combine the shadow and the image
    image_with_shadow = Image.alpha_composite(shadow, image)
    return image_with_shadow

def apply_syntax_highlighting(code, lexer_name='bash'):
    # Apply syntax highlighting to the code
    lexer = get_lexer_by_name(lexer_name)
    formatter = ImageFormatter(style='monokai', line_numbers=False)
    return highlight(code, lexer, formatter)

def main():
    # Main function to process the log file and create the image
    log_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    add_drop_shadow = len(sys.argv) > 3 and sys.argv[3].lower() == "--drop-shadow"
    
    padding = (20, 20, 10, 40)
    text_color = (187, 187, 187)
    bg_color = (39, 40, 34)  # Monokai background color
    font_size = 16
    
    # Read the log file
    log_text = read_log_file(log_file_path)
    
    # Apply syntax highlighting
    highlighted_code = apply_syntax_highlighting(log_text)
    
    # Create an image from the highlighted code
    font = get_font(font_size)
    text_lines_padded = add_padding(highlighted_code, padding)
    img_size = get_image_size(font, text_lines_padded, padding)
    img = create_image(highlighted_code, font, img_size, bg_color, text_color, padding)
    
    # Apply drop shadow effect if requested
    if add_drop_shadow:
        img = drop_shadow(img)
    
    # Save the image to disk
    save_image(img, output_file_path)


if __name__ == "__main__":
    main()