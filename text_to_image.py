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
    text_lines_padded = [" " * padding[0] + line + " " * padding[2] for line in text_lines]
    text_lines_padded.append(" " * padding[0])  # add a blank line for padding at the bottom
    return text_lines_padded


def get_image_size(font, text_lines_padded, padding):
    line_height = int(font.getbbox("A")[3])
    img_width = int(max(font.getbbox(line)[2] for line in text_lines_padded) + padding[0] + padding[2])
    img_height = int(line_height * len(text_lines_padded) + padding[0] + padding[3])
    return img_width, img_height


def create_image(highlighted_code, font, img_size, bg_color, text_color, padding):
    # Create a new RGBA image with the given size and background color
    img = Image.new("RGBA", img_size, bg_color)
    draw = ImageDraw.Draw(img)
    # Draw the highlighted text onto the image
    draw_highlighted_text(highlighted_code, draw, font, text_color, padding)
    return img


def highlight_text(text, font):
    style = get_style_by_name("monokai")
    lexer = get_lexer_by_name("console", stripall=True)
    formatter = ImageFormatter(font=font, style=style)
    highlighted_code = highlight(text, lexer, formatter)
    return highlighted_code

def draw_highlighted_text(highlighted_text, draw, font, text_color, padding):
    # Draw the highlighted text onto the image
    x = padding[0]
    y = padding[0]
    for line in highlighted_text.splitlines():
        line_bbox = draw.textbbox((x, y), line, font=font, stroke_width=0)
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_bbox[3] - line_bbox[1]

def save_image(image, output_file_path):
    image.save(output_file_path)


def main():
    log_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    padding = (20, 20, 20, 40)
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

    # save the image to disk
    save_image(img, output_file_path)

def drop_shadow(image):
    # create a new image for the drop shadow
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    # create a draw object for the shadow
    draw = ImageDraw.Draw(shadow)
    # create a mask for the original image
    mask = Image.new("RGBA", image.size, (0, 0, 0, 255))
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rectangle((3, 3, mask.size[0] + 3, mask.size[1] + 3), fill=(255, 255, 255, 0))
    # draw the shadow
    for x in range(-3, 4):
        for y in range(-3, 4):
            draw.bitmap((x + 3, y + 3), image.convert("L"), fill=(0, 0, 0, 15))
    # combine the shadow and the image
    return image

def main():
    log_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    padding = (20, 20, 20, 40)
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
    # save the image to disk
    save_image(img, output_file_path)

if __name__ == "__main__":
    main()
    