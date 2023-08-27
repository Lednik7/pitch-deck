import os 
from positions import positions as p
import streamlit as st
import urllib.request
from PIL import Image, ImageFont, ImageDraw 

import warnings
warnings.filterwarnings('ignore')


@st.cache_data()
def use_color(c='black'):
    for attr in dir(p):
        if attr.endswith("_color"):
            setattr(p, attr, c) 
            
       
@st.cache_data()     
def generate_style_test(prompt):
    print(f'generating style by {prompt}')
    
    base = """Slidesgo, Freepik. Pinterest. More white. Maybe gradient. WITHOUT TEXT. Vectors style. WITHOUT TEXT. Image for PowerPoint background. Gradientdip. More game with colors. smooth transition. smooth transition. smooth transition"""
    URL = f"http://141.105.64.158:8730/images"
    
    output_path = '_'.join(prompt.split())
    try:
        os.mkdir(f'out/{output_path}')
    except:
        pass
    
    with st.spinner('Генерируем, не перезагружайте страницу...'):
        i = 1
            
        headers = {
            "query": prompt+' '+base,
            "negative": ""
        }

        req = urllib.request.Request(URL, headers=headers)
        with urllib.request.urlopen(req) as url:
            img = Image.open(url)
            
        img = img.resize((1920, 1080))
        img.save(f'out/{output_path}/1.png')
        return img
    
    
@st.cache_data()     
def continue_generating_style_test(prompt):
    print(f'continue generating style by {prompt}')
    
    base = """Slidesgo, Freepik. Pinterest. More white. Maybe gradient. WITHOUT TEXT. Vectors style. WITHOUT TEXT. Image for PowerPoint background. Gradientdip. More game with colors. smooth transition. smooth transition. smooth transition"""
    URL = f"http://141.105.64.158:8730/images"
    
    output_path = '_'.join(prompt.split())
    try:
        os.mkdir(f'out/{output_path}')
    except:
        pass
    
    with st.spinner('Генерируем, не перезагружайте страницу...'):
        for i in range(2, 12):
            
            headers = {
                "query": prompt+' '+base,
                "negative": ""
            }

            req = urllib.request.Request(URL, headers=headers)
            with urllib.request.urlopen(req) as url:
                img = Image.open(url)
                
            img.resize((1920, 1080)).save(f'out/{output_path}/{i}.png')
    
    return f'out/{output_path}/'
            

def split_string_evenly(s, coords, adjust=0):
    if len(s.split()) == 1:
        coords = (coords[0], coords[1]+adjust)
        return s, coords
    # Find the middle index
    mid = len(s) // 2
    
    # Find the nearest space to the left and right of the middle
    left_space = s.rfind(' ', 0, mid)
    right_space = s.find(' ', mid)
    
    # Determine which space is closer to the middle
    if mid - left_space < right_space - mid:
        split_index = left_space
    else:
        split_index = right_space
        
    return s[:split_index] + '\n' + s[split_index+1:], coords  


def add_text_to_image(img, text, coords=None, max_symbols=None,
                      font_path=None, font_size=None,
                      align='left', color='black'):
    # Create drawing context
    draw = ImageDraw.Draw(img)
    
    # Load font
    font = ImageFont.truetype('fonts/'+font_path, font_size)
    
    # Add text to the image
    draw.text(coords, text, fill=color, font=font, align=align)
    
    return img

def add_text_to_image(img, text, coords=None, max_symbols=None,
                      font_path=None, font_size=None,
                      align='left', color='black'):
    # Create drawing context
    draw = ImageDraw.Draw(img)
    
    # Load font
    font = ImageFont.truetype('fonts/'+font_path, font_size)
    
    # Add text to the image
    draw.text(coords, text, fill=color, font=font, align=align)
    
    return img

def split_text_by_px_width(s, font, block_width_px):
    words = s.split()
    lines = []
    current_line = []
    current_length_px = 0

    for word in words:
        word_length_px = font.getsize(word)[0]
        
        if current_length_px + word_length_px <= block_width_px:
            current_length_px += word_length_px + font.getsize(' ')[0]  # Add space width
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length_px = word_length_px + font.getsize(' ')[0]

    if current_line:  # Add any remaining words
        lines.append(' '.join(current_line))

    return '\n'.join(lines)

@st.cache_data(show_spinner=False)
def get_slide_1(img, title, subtitle, color):
    title_text, title = split_string_evenly(title, p.title1, 120)
    img = add_text_to_image(
                            img, 
                            title_text, 
                            title, 
                            p.title1_max_symbols, 
                            p.title1_font, 
                            round(p.title1_font_size*1.36), 
                            p.title1_align, 
                            color
                            )

    img = add_text_to_image(
                            img, 
                            subtitle, 
                            p.subtitle1, 
                            p.subtitle1_max_symbols, 
                            p.subtitle1_font, 
                            round(p.subtitle1_font_size*1.36), 
                            p.subtitle1_align, 
                            color
                           )
    
    return img

@st.cache_data(show_spinner=False)
def get_slide2(img, title, text, color):
    title_text, title = split_string_evenly(title, p.title2, 30)
    img = add_text_to_image(
                        img, 
                        title_text, 
                        title, 
                        p.title2_max_symbols, 
                        p.title2_font, 
                        round(p.title2_font_size*1.36), 
                        p.title2_align, 
                        color
                        )

    font_path = p.text2_font  # You must point to a TrueType font file
    font_size = round(p.text2_font_size*1.36)  # Change this to your desired font size
    font = ImageFont.truetype('fonts/'+font_path, font_size)
    block_width = p.text2_block_width
    text = split_text_by_px_width(text, font, block_width)
    
    img = add_text_to_image(
                            img, 
                            text, 
                            p.text2, 
                            p.text2_max_symbols, 
                            p.text2_font, 
                            round(p.text2_font_size*1.36), 
                            p.text2_align, 
                            color
                           )
        
    return img

 
@st.cache_data(show_spinner=False)
def get_slide_3(img, title, subtitle1, subtitle2, text1, text2, color):
    title_text, title = split_string_evenly(title, p.title3)
    img = add_text_to_image(
                        img, 
                        title_text, 
                        title, 
                        p.title3_max_symbols, 
                        p.title3_font, 
                        round(p.title3_font_size*1.36), 
                        p.title3_align, 
                        color
                        )
    
    img = add_text_to_image(
                            img, 
                            subtitle1, 
                            p.subtitle3_1, 
                            p.subtitle3_1_max_symbols, 
                            p.subtitle3_1_font, 
                            round(p.subtitle3_1_font_size*1.36), 
                            p.subtitle3_1_align, 
                            color
                           )
    
    img = add_text_to_image(
                            img, 
                            subtitle2, 
                            p.subtitle3_2, 
                            p.subtitle3_2_max_symbols, 
                            p.subtitle3_2_font, 
                            round(p.subtitle3_2_font_size*1.36), 
                            p.subtitle3_2_align, 
                            color
                           )
    
    font_path = p.text3_1_font  # You must point to a TrueType font file
    font_size = round(p.text3_1_font_size*1.36)  # Change this to your desired font size
    font = ImageFont.truetype('fonts/'+font_path, font_size)
    
    text1 = split_text_by_px_width(text1, font, p.text3_1_block_width)
    text2 = split_text_by_px_width(text2, font, p.text3_2_block_width)
    
    img = add_text_to_image(
                            img, 
                            text1, 
                            p.text3_1, 
                            p.text3_1_max_symbols, 
                            p.text3_1_font, 
                            round(p.text3_1_font_size*1.36), 
                            p.text3_1_align, 
                            color
                           )
    img = add_text_to_image(
                            img, 
                            text2, 
                            p.text3_2, 
                            p.text3_2_max_symbols, 
                            p.text3_2_font, 
                            round(p.text3_2_font_size*1.36), 
                            p.text3_2_align, 
                            color
                           )
    
    return img

 
@st.cache_data(show_spinner=False)
def get_slide_4(img, title, subtitle1, subtitle2, subtitle3, text1, text2, text3, color):
    # title_text, title = split_string_evenly(title, p.title4)
    img = add_text_to_image(
                        img, 
                        title, 
                        p.title4,
                        p.title4_max_symbols, 
                        p.title4_font, 
                        round(p.title4_font_size*1.36), 
                        p.title4_align, 
                        color
                        )
    
    img = add_text_to_image(
                            img, 
                            subtitle1, 
                            p.subtitle4_1, 
                            p.subtitle4_1_max_symbols, 
                            p.subtitle4_1_font, 
                            round(p.subtitle4_1_font_size*1.36), 
                            p.subtitle4_1_align, 
                            color
                           )
    
    img = add_text_to_image(
                            img, 
                            subtitle2, 
                            p.subtitle4_2, 
                            p.subtitle4_2_max_symbols, 
                            p.subtitle4_2_font, 
                            round(p.subtitle4_2_font_size*1.36), 
                            p.subtitle4_2_align, 
                            color
                           )
    
    img = add_text_to_image(
                            img, 
                            subtitle3, 
                            p.subtitle4_3, 
                            p.subtitle4_3_max_symbols, 
                            p.subtitle4_3_font, 
                            round(p.subtitle4_3_font_size*1.36), 
                            p.subtitle4_3_align, 
                            color
                           )
    
    font_path = p.text4_1_font  # You must point to a TrueType font file
    font_size = round(p.text4_1_font_size*1.36)  # Change this to your desired font size
    font = ImageFont.truetype('fonts/'+font_path, font_size)
    
    text1 = split_text_by_px_width(text1, font, p.text4_1_block_width)
    text2 = split_text_by_px_width(text2, font, p.text4_2_block_width)
    text3 = split_text_by_px_width(text3, font, p.text4_3_block_width)
    
    img = add_text_to_image(
                            img, 
                            text1, 
                            p.text4_1, 
                            p.text4_1_max_symbols, 
                            p.text4_1_font, 
                            round(p.text4_1_font_size*1.36), 
                            p.text4_1_align, 
                            color
                           )
    img = add_text_to_image(
                            img, 
                            text2, 
                            p.text4_2, 
                            p.text4_2_max_symbols, 
                            p.text4_2_font, 
                            round(p.text4_2_font_size*1.36), 
                            p.text4_2_align, 
                            color
                           )
    img = add_text_to_image(
                            img, 
                            text3, 
                            p.text4_3, 
                            p.text4_3_max_symbols, 
                            p.text4_3_font, 
                            round(p.text4_3_font_size*1.36), 
                            p.text4_3_align, 
                            color
                           )
    
    return img

 
@st.cache_data(show_spinner=False) 
def get_slide_5(img, title, text1, color):
    # title_text, title = split_string_evenly(title, p.title5)
    img = add_text_to_image(
                        img, 
                        title, 
                        p.title5,
                        p.title5_max_symbols, 
                        p.title5_font, 
                        round(p.title5_font_size*1.36), 
                        p.title5_align, 
                        color
                        )
    
    
    font_path = p.text5_font  # You must point to a TrueType font file
    font_size = round(p.text5_font_size*1.36)  # Change this to your desired font size
    font = ImageFont.truetype('fonts/'+font_path, font_size)
    
    text1 = split_text_by_px_width(text1, font, p.text5_block_width)
    
    img = add_text_to_image(
                            img, 
                            text1, 
                            p.text5, 
                            p.text5_max_symbols, 
                            p.text5_font, 
                            round(p.text5_font_size*1.36), 
                            p.text5_align, 
                            color
                           )
    
    return img

 
@st.cache_data(show_spinner=False)
def get_slide_6(img, title, text1, color):
    # title_text, title = split_string_evenly(title, p.title5)
    img = add_text_to_image(
                        img, 
                        title, 
                        p.title6,
                        p.title6_max_symbols, 
                        p.title6_font, 
                        round(p.title6_font_size*1.36), 
                        p.title6_align, 
                        color
                        )
    
    
    font_path = p.text6_font  # You must point to a TrueType font file
    font_size = round(p.text6_font_size*1.36)  # Change this to your desired font size
    font = ImageFont.truetype('fonts/'+font_path, font_size)
    
    text1 = split_text_by_px_width(text1, font, p.text6_block_width)
    
    img = add_text_to_image(
                            img, 
                            text1, 
                            p.text6, 
                            p.text6_max_symbols, 
                            p.text6_font, 
                            round(p.text6_font_size*1.36), 
                            p.text6_align, 
                            color
                           )
    return img
    

 
@st.cache_data(show_spinner=False)
def get_slide_7(img, title, text1, color):
    # title_text, title = split_string_evenly(title, p.title7, 30)
    img = add_text_to_image(
                        img, 
                        title, 
                        p.title7,
                        p.title7_max_symbols, 
                        p.title7_font, 
                        round(p.title7_font_size*1.36), 
                        p.title7_align, 
                        color
                        )
    
    
    font_path = p.text7_font  # You must point to a TrueType font file
    font_size = round(p.text7_font_size*1.36)  # Change this to your desired font size
    font = ImageFont.truetype('fonts/'+font_path, font_size)
    
    text1 = split_text_by_px_width(text1, font, p.text7_block_width)
    
    img = add_text_to_image(
                            img, 
                            text1, 
                            p.text7, 
                            p.text7_max_symbols, 
                            p.text7_font, 
                            round(p.text7_font_size*1.36), 
                            p.text7_align, 
                            color
                           )
    
    return img

 
@st.cache_data(show_spinner=False)
def get_slide_8(img, title, text1, color):
    # title_text, title = split_string_evenly(title, p.title8)
    img = add_text_to_image(
                        img, 
                        title, 
                        p.title8,
                        p.title8_max_symbols, 
                        p.title8_font, 
                        round(p.title8_font_size*1.36), 
                        p.title8_align, 
                        color
                        )
    
    
    font_path = p.text8_font  # You must point to a TrueType font file
    font_size = round(p.text8_font_size*1.36)  # Change this to your desired font size
    font = ImageFont.truetype('fonts/'+font_path, font_size)
    
    text1 = split_text_by_px_width(text1, font, p.text8_block_width)
    
    img = add_text_to_image(
                            img, 
                            text1, 
                            p.text8, 
                            p.text8_max_symbols, 
                            p.text8_font, 
                            round(p.text8_font_size*1.36), 
                            p.text8_align, 
                            color
                           )
    return img

 
@st.cache_data(show_spinner=False)
def get_slide_9(img, title, text1, color):
    # title_text, title = split_string_evenly(title, p.title8)
    img = add_text_to_image(
                        img, 
                        title, 
                        p.title9,
                        p.title9_max_symbols, 
                        p.title9_font, 
                        round(p.title9_font_size*1.36), 
                        p.title9_align, 
                        color
                        )
    
    
    # font_path = p.text9_font  # You must point to a TrueType font file
    # font_size = round(p.text9_font_size*1.36)  # Change this to your desired font size
    # font = ImageFont.truetype('fonts/'+font_path, font_size)
    
    # text1 = split_text_by_px_width(text1, font, p.text9_block_width)
    
    img = add_text_to_image(
                            img, 
                            text1, 
                            p.text9, 
                            p.text9_max_symbols, 
                            p.text9_font, 
                            round(p.text9_font_size*1.36), 
                            p.text9_align, 
                            color
                           )
    return img

 
def add_photo_to_image(base_image, photo, x, y, w, h):
    
    # Resize the photo
    photo = photo.resize((w, h))
    
    # Paste the photo onto the main image
    base_image.paste(photo, (x, y))
    
    return base_image

 
def get_slide_10(img, title1, title2, photo, subtitle1, subtitle2, color):
    img = add_text_to_image(
                        img, 
                        title1, 
                        p.title10_1, 
                        p.title10_1_max_symbols, 
                        p.title10_1_font, 
                        round(p.title10_1_font_size*1.36), 
                        p.title10_1_align, 
                        color
                        )
    font_path = p.title10_2_font  # You must point to a TrueType font file
    font_size = round(p.title10_2_font_size*1.36)  # Change this to your desired font size
    font = ImageFont.truetype('fonts/'+font_path, font_size)
    
    title2 = split_text_by_px_width(title2, font, 914)
    img = add_text_to_image(
                        img, 
                        title2, 
                        p.title10_2, 
                        p.title10_2_max_symbols, 
                        p.title10_2_font, 
                        round(p.title10_2_font_size*1.36), 
                        p.title10_2_align, 
                        color
                        )
    
    img = add_photo_to_image(img, photo, p.photo10[0], p.photo10[1], p.photo10_w, p.photo10_h)
    
    img = add_text_to_image(
                            img, 
                            subtitle1, 
                            p.subtitle10_1, 
                            p.subtitle10_1_max_symbols, 
                            p.subtitle10_1_font, 
                            round(p.subtitle10_1_font_size*1.36), 
                            p.subtitle10_1_align, 
                            color
                           )
    
    img = add_text_to_image(
                            img, 
                            subtitle2, 
                            p.subtitle10_2, 
                            p.subtitle10_2_max_symbols, 
                            p.subtitle10_2_font, 
                            round(p.subtitle10_2_font_size*1.36), 
                            p.subtitle10_2_align, 
                            color
                           )
    
    return img

 
@st.cache_data(show_spinner=False) 
def get_slide_11(img, title, subtitle, color):
    # title_text, title = split_string_evenly(title, p.title8)
    img = add_text_to_image(
                        img, 
                        title, 
                        p.title11,
                        p.title11_max_symbols, 
                        p.title11_font, 
                        round(p.title11_font_size*1.36), 
                        p.title11_align, 
                        color
                        )
    
    img = add_text_to_image(
                            img, 
                            subtitle, 
                            p.subtitle11, 
                            p.subtitle11_max_symbols, 
                            p.subtitle11_font, 
                            round(p.subtitle11_font_size*1.36), 
                            p.subtitle11_align, 
                            color
                           )
    
    return img