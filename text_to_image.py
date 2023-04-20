import sys
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.img import ImageFormatter
from pygments.styles import get_style_by_name


def get_token_style(token):
    style = get_style_by_name("monokai")
    return style.style_for_token(token)

def read_log_file(log_file_path):
    #Used to read in the contents of the log file passed in the argument below
    with open(log_file_path, "r") as f:
        return f.read()

def get_font(font_size):
    font_file = os.path.join(os.getcwd(), "DejaVuSansMono.ttf")
    try:
        return ImageFont.truetype(font_file, font_size)
    except OSError:
        font_file = os.path.join(os.getcwd(), "./support/DejaVuSansMono.ttf")
        return ImageFont.truetype(font_file, font_size)

def add_padding(text, padding):
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
    line_height = int(font.getbbox("A")[3])
    img_width = int(max(font.getbbox(line)[2] for line in text_lines_padded) + padding[0] + padding[2])
    img_height = int(line_height * len(text_lines_padded) + padding[0] + padding[3])
    return img_width, img_height

def create_image(highlighted_code, font, img_size, bg_color, text_color, padding):
    # Define the border size and color
    border_width = 25
    border_color = (60, 60, 60)
    # Define the inner rectangle size and position
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
    # Draw the minimize button
    button_pos = (bar_pos[0] + bar_size[0] - 80, bar_pos[1] + 5)
    button_size = (20, 20)
    draw.rectangle((button_pos, tuple(map(sum, zip(button_pos, button_size)))), fill=(239, 184, 56))
    # Draw the resize button
    button_pos = (bar_pos[0] + bar_size[0] - 50, bar_pos[1] + 5)
    button_size = (20, 20)
    draw.rectangle((button_pos, tuple(map(sum, zip(button_pos, button_size)))), fill=(122, 189, 83))
    # Draw the close button
    button_pos = (bar_pos[0] + bar_size[0] - 20, bar_pos[1] + 5)
    button_size = (20, 20)
    draw.rectangle((button_pos, tuple(map(sum, zip(button_pos, button_size)))), fill=(226, 56, 62))
    # Draw the highlighted text onto the image
    y_offset = title_text_pos[1] + title_text_bbox[3] + padding[1]
    draw_highlighted_text(highlighted_code, draw, font, text_color, (padding[0] + inner_rect_pos[0], y_offset))
    return img

def draw_highlighted_text(highlighted_text, draw, font, text_color, padding):
    # Draw the highlighted text onto the image
    x = padding[0]
    y = padding[1]
    for line in highlighted_text.splitlines():
        line_bbox = draw.textbbox((x, y), line, font=font, stroke_width=0)
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_bbox[3] - line_bbox[1] + 1

def save_image(image, output_file_path):
    image.save(output_file_path)


def drop_shadow(image):
    # create a new image for the drop shadow
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    # create a draw object for the shadow
    draw = ImageDraw.Draw(shadow)
    # create a mask for the original image
    mask = Image.new("L", image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rectangle((3, 3, mask.size[0] + 3, mask.size[1] + 3), fill=255)
    # draw the shadow
    for x in range(-3, 1):
        for y in range(-3, 1):
            draw.bitmap((x + 3, y + 3), image.convert("L"), fill=(0, 0, 0, 25))
    # combine the shadow and the image
    image_with_shadow = Image.alpha_composite(image, shadow)
    return image_with_shadow

def main():
    log_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3].lower() == "--drop-shadow":
        add_drop_shadow = True
    else:
        add_drop_shadow = False
    padding = (20, 20, 10, 40)
    text_color = (187, 187, 187)
    bg_color = (0, 0, 0)
    font_size = 16
    # read in the log file
    log_text = read_log_file(log_file_path)
    # create an image from the log text
    font = get_font(font_size)
    text_lines_padded = add_padding(log_text, padding)
    img_size = get_image_size(font, text_lines_padded, padding)
    img = create_image(log_text, font, img_size, bg_color, text_color, padding)
    # apply drop shadow effect if requested
    if add_drop_shadow:
        img = drop_shadow(img)
    # save the image to disk
    save_image(img, output_file_path)


if __name__ == "__main__":
    main()
    