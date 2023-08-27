import streamlit as st
from streamlit_image_select import image_select
from googletrans import Translator
from utils import *
from PIL import Image, ImageFont, ImageDraw 
from llama import ask_llama_slide2, ask_llama_slide3, ask_llama_slide4, ask_llama_slide5, ask_llama_slide6, ask_llama_slide7, ask_llama_slide8, ask_llama_slide_text, ask_llama_assist, make_letter_for_investor
import img2pdf


translator = Translator()

@st.cache_data(show_spinner=False)
def get_translation(text, dest='en'):
    return translator.translate(text, dest=dest).text

st.set_page_config(layout="wide")
st.title('Аппаратное :blue[ускорение] :sunglasses:')
texts = ["Основные настройки", "Название проекта", "Проблема", "Описание",
         "Решение", "Рынок", "Цели", "Конкуренты", "Бизнес-модель", "Инвестиции",
         "Команда", "Контакты", "Экспортировать"]

template_paths = ['../generated_5/', '../generated_9/', '../generated_10/', '../template2/', '../template1/', '../template3/']

if 'selected_image' not in st.session_state:
    st.session_state.selected_image = None

if 'test_gen_img' not in st.session_state:
    st.session_state.test_gen_img = None
    
if 'output_path' not in st.session_state:
    st.session_state.output_path = None
    
if 'prompt' not in st.session_state:
    st.session_state.prompt = None
    
if 'full_data' not in st.session_state:
    st.session_state.full_data = {}
    
if 'pptx_text' not in st.session_state:
    st.session_state.pptx_text = ''
    
if 'letter_text' not in st.session_state:
    st.session_state.letter_text = ''
    
tabs = st.tabs(texts)
for idx, tab in enumerate(tabs):
    if idx == 0:
        with tab:
            prompt = get_translation(st.text_input('Создать свой стиль. Введите запрос для генерации (Kandinsky 2.2)', placeholder='Минималистичное, сине градиентное сияние'))
            if prompt != st.session_state.prompt:
                st.session_state.prompt = prompt
                st.session_state.output_path = None
            
            if st.session_state.prompt:
                if st.button('Генерировать свой стиль', use_container_width=True, type='primary'):
                    st.session_state.test_gen_img = generate_style_test(st.session_state.prompt)
                    
                if st.session_state.test_gen_img:
                    col1_gen, col2_gen = st.columns(2)
                    
                    col1_gen.image(st.session_state.test_gen_img, caption=f'Сгенерированный стиль по запросу {st.session_state.prompt}')
                    if col1_gen.button('Продолжить генерацию', use_container_width=True, type='primary'):
                        st.session_state.output_path = continue_generating_style_test(st.session_state.prompt)
                        
                    if st.session_state.output_path:
                        col1, col2, col3, col4, col5 = col2_gen.columns(5)
                        col1.image(st.session_state.output_path+'2.png')
                        col2.image(st.session_state.output_path+'3.png')
                        col3.image(st.session_state.output_path+'4.png')
                        col4.image(st.session_state.output_path+'5.png')
                        col5.image(st.session_state.output_path+'6.png')
                        
                        col1, col2, col3, col4, col5 = col2_gen.columns(5)
                        col1.image(st.session_state.output_path+'7.png')
                        col2.image(st.session_state.output_path+'8.png')
                        col3.image(st.session_state.output_path+'9.png')
                        col4.image(st.session_state.output_path+'10.png')
                        col5.image(st.session_state.output_path+'11.png')
                        
                        if col2_gen.button('Использовать стиль', use_container_width=True, type='primary'):
                            st.session_state.selected_image = st.session_state.output_path
                            print(st.session_state.selected_image)
            
            if not st.session_state.test_gen_img or not st.session_state.prompt:
                selected_image_style = image_select("Выберите готовый стиль", ["../generated_5/1.png", "../generated_9/1.png", "../generated_10/1.png", "../template2/1.png", "../template1/1.png"])
                st.session_state.selected_image = '/'.join(selected_image_style.split('/')[:-1])+'/'
    else:
        with tab:
            if idx != 12:
                if idx == 1:
                    data = st.text_input(label=texts[idx], max_chars=25)
                elif idx == 9:
                    data = st.text_input(label='Необходимая сумма: ($)')
                    manufacture_percent = st.slider('Процент на производство и материалы', 0, 100, 50)
                    marketing_percent = st.slider('Процент на маркетинг и продажи', 0, 100, 25)
                    research_percent = st.slider('Процент на исследование и разработку', 0, 100, 15)
                    other_percent = st.slider('Процент на зарплаты и административные расходы', 0, 100, 10)
                elif idx == 10:
                    photo_file = st.file_uploader("Загрузите фото выступающего")
                    col1, col2 = st.columns(2)
                    data = col1.text_input(label='Введите ФИ выступающего', max_chars=25)
                    position10 = col2.text_input(label='Введите должность выступающего', max_chars=25)
                    employe_amount = st.slider('Количество работников', 1, 1000, 50)
                elif idx == 11:
                    col1, col2, col3 = st.columns(3)
                    data = col1.text_input(label='Введите ваш веб-сайт')
                    email = col2.text_input(label='Введите ваш корпоративный email')
                    tell_number = col3.text_input('Введите ваш корпоративный номер телефона (Опционально)')
                else:   
                    data = st.text_area(label=texts[idx])
                    
                col1_main, col2_main = st.columns(2)
                color = col1_main.selectbox('Цвет текста на слайде', ['Черный', 'Белый'], key=f'select-box{idx}')
                color = 'black' if color == 'Черный' else 'white'
                
                try:
                    os.mkdir(f"final_out/{st.session_state.selected_image.split('/')[1]}")
                except:
                    pass

                # with col1_main:
                if st.session_state.selected_image:
                    img = Image.open(f"{st.session_state.selected_image}{idx}.png").resize((1920, 1080))
                    
                    other_style_images = []
                    for path in template_paths:
                        other_style_images.append(Image.open(f"{path}{idx}.png").resize((1920, 1080)))
                    
                    if idx == 1 and data:
                        p.title1_color = color
                        p.subtitle1_color = color
                        
                        print(color)
                        img = get_slide_1(img, data, 'Эта презентация вам понравится!', color)
                        col1_main.image(img)
                        
                        st.session_state.full_data['Эта презентация вам понравится!'] = data
                        
                        save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                        if save_slide:
                            img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                        
                        col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                        cols = [col1, col2, col3, col4, col5, col6]
                        for img_id, col in enumerate(cols):
                            col.image(get_slide_1(other_style_images[img_id], data, 'Эта презентация вам понравится!', color))
                        
                    elif idx == 2 and data:
                        p.title2_color = color
                        p.text2_color = color
                        
                        assist = col2_main.text_area(label="Ассистент-редактор", key=idx, placeholder="Пример: Перефразируй текст")
                        
                        if not assist:
                            text2 = ask_llama_slide2(data)
                            img = get_slide2(img, 'Проблема', text2, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Проблема'] = text2
                            
                            text_prompt = f"Эта презентация вам понравится!: {st.session_state.full_data['Эта презентация вам понравится!']}" + ' ' f"Проблема: {text2}"
                            st.session_state.pptx_text = ask_llama_slide_text(text_prompt)
                            st.session_state.letter_text = make_letter_for_investor(text_prompt[text_prompt.index(':')+2:])
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide2(other_style_images[img_id], 'Проблема', text2, color))
                        else:
                            text2 = ask_llama_assist(assist, st.session_state.full_data['Проблема'])
                            img = get_slide2(img, 'Проблема', text2, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Проблема'] = text2
                            
                            text_prompt = f"Эта презентация вам понравится!: {st.session_state.full_data['Эта презентация вам понравится!']}" + ' ' f"Проблема: {text2}"
                            st.session_state.pptx_text = ask_llama_slide_text(text_prompt)
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide2(other_style_images[img_id], 'Проблема', text2, color))
                            
                    elif idx == 3 and data:
                        p.title3_color = color
                        p.subtitle3_1_color = color
                        p.text3_1_color = color
                        p.subtitle3_2_color = color
                        p.text3_2_color = color
                        
                        assist = col2_main.text_area(label="Ассистент-редактор", key=idx, placeholder="Пример: Перефразируй текст")
                        
                        if not assist:
                            text3_1, text3_2 = ask_llama_slide3(data)
                            img = get_slide_3(img, 'Ценностное предложения стартапа', 'Идея стартапа', 'Что мы хотим', text3_1, text3_2, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Ценностное предложения стартапа'] = text3_1 + ' | ' + text3_2
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Ценностное предложения стартапа: {text3_1 + ' ' + text3_2}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_3(other_style_images[img_id], 'Ценностное предложения стартапа', 'Идея стартапа', 'Что мы хотим', text3_1, text3_2, color))
                        else:
                            text3_1 = ask_llama_assist(assist, st.session_state.full_data['Ценностное предложения стартапа'].split(' | ')[0])
                            text3_2 = ask_llama_assist(assist, st.session_state.full_data['Ценностное предложения стартапа'].split(' | ')[1])
                            img = get_slide_3(img, 'Ценностное предложения стартапа', 'Идея стартапа', 'Что мы хотим', text3_1, text3_2, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Ценностное предложения стартапа'] = text3_1 + ' | ' + text3_2
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Ценностное предложения стартапа: {text3_1 + ' ' + text3_2}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_3(other_style_images[img_id], 'Ценностное предложения стартапа', 'Идея стартапа', 'Что мы хотим', text3_1, text3_2, color))
                            
                    elif idx == 4 and data:
                        p.title4_color = color
                        p.subtitle4_1_color = color
                        p.text4_1_color = color
                        p.subtitle4_2_color = color
                        p.text4_2_color = color
                        p.subtitle4_3_color = color
                        p.text4_3_color = color
                        
                        assist = col2_main.text_area(label="Ассистент-редактор", key=idx, placeholder="Пример: Перефразируй текст")
                        
                        if not assist:
                            text4_1, text4_2, text4_3, subtitle1, subtitle2, subtitle3 = ask_llama_slide4(data)
                            img = get_slide_4(img, 'Решение', subtitle1, subtitle2, subtitle3, text4_1, text4_2, text4_3, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Решение'] = text4_1 + ' | ' + text4_2 + ' | ' + text4_3
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Решение: {text4_1 + ' ' + text4_2 + ' ' + text4_3}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_4(other_style_images[img_id], 'Решение', subtitle1, subtitle2, subtitle3, text4_1, text4_2, text4_3, color))
                        else:
                            text4_1 = ask_llama_assist(assist, st.session_state.full_data['Решение'].split(' | ')[0])
                            text4_2 = ask_llama_assist(assist, st.session_state.full_data['Решение'].split(' | ')[1])
                            text4_3 = ask_llama_assist(assist, st.session_state.full_data['Решение'].split(' | ')[2])
                            img = get_slide_4(img, 'Решение', subtitle1, subtitle2, subtitle3, text4_1, text4_2, text4_3, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Решение'] = text4_1 + ' | ' + text4_2 + ' | ' + text4_3
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Решение: {text4_1 + ' ' + text4_2 + ' ' + text4_3}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_4(other_style_images[img_id], 'Решение', subtitle1, subtitle2, subtitle3, text4_1, text4_2, text4_3, color))
                            
                    elif idx == 5 and data:
                        p.title5_color = color
                        p.text5_color = color
                        
                        assist = col2_main.text_area(label="Ассистент-редактор", key=idx, placeholder="Пример: Перефразируй текст")
                            
                        if not assist:
                            text5 = ask_llama_slide5(data)
                            img = get_slide_5(img, 'Анализ рынка', text5, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Анализ рынка'] = text5
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Анализ рынка: {text5}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_5(other_style_images[img_id], 'Анализ рынка', text5, color))
                        else:
                            text5 = ask_llama_assist(assist, st.session_state.full_data['Анализ рынка'])
                            img = get_slide_5(img, 'Анализ рынка', text5, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Анализ рынка'] = text5
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Анализ рынка: {text5}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_5(other_style_images[img_id], 'Анализ рынка', text5, color))
                            
                    elif idx == 6 and data:
                        p.title6_color = color
                        p.text6_color = color
                            
                        assist = col2_main.text_area(label="Ассистент-редактор", key=idx, placeholder="Пример: Перефразируй текст")
                            
                        if not assist:
                            text6 = ask_llama_slide6(data)
                            img = get_slide_6(img, 'Цели', text6, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Цели'] = text6
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Цели: {text6}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_6(other_style_images[img_id], 'Цели', text6, color))
                        else:
                            text6 = ask_llama_assist(assist, st.session_state.full_data['Цели'])
                            img = get_slide_6(img, 'Цели', text6, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Цели'] = text6
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Цели: {text6}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_6(other_style_images[img_id], 'Цели', text6, color))
                            
                    elif idx == 7 and data:
                        p.title7_color = color
                        p.text7_color = color
                            
                        assist = col2_main.text_area(label="Ассистент-редактор", key=idx, placeholder="Пример: Перефразируй текст")
                            
                        if not assist:
                            text7 = ask_llama_slide7(st.session_state.full_data['Ценностное предложения стартапа'])
                            img = get_slide_7(img, 'Конкурентные преимущества', text7, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Конкурентные преимущества'] = text7
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Конкурентные преимущества: {text7}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_7(other_style_images[img_id], 'Конкурентные преимущества', text7, color))
                        else:
                            text7 = ask_llama_assist(assist, st.session_state.full_data['Конкурентные преимущества'])
                            img = get_slide_7(img, 'Конкурентные преимущества', text7, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Конкурентные преимущества'] = text7
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Конкурентные преимущества: {text7}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_7(other_style_images[img_id], 'Конкурентные преимущества', text7, color))
                            
                    elif idx == 8 and data:
                        p.title8_color = color
                        p.text8_color = color
                            
                        assist = col2_main.text_area(label="Ассистент-редактор", key=idx, placeholder="Пример: Перефразируй текст")
                            
                        if not assist:
                            text8 = ask_llama_slide8(st.session_state.full_data['Ценностное предложения стартапа'])
                            img = get_slide_8(img, 'Бизнес-модель', text8, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Бизнес-модель'] = text8
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Бизнес-модель: {text8}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_8(other_style_images[img_id], 'Бизнес-модель', text8, color))
                        else:
                            text8 = ask_llama_assist(assist, st.session_state.full_data['Бизнес-модель'])
                            img = get_slide_8(img, 'Бизнес-модель', text8, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Бизнес-модель'] = text8
                            st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Бизнес-модель: {text8}")
                            
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_8(other_style_images[img_id], 'Бизнес-модель', text8, color))
                            
                    elif idx == 9 and data:
                        p.title9_color = color
                        p.text9_color = color
                        
                        text9 = f"""Необходимая сумма: ${data}\n
                        * На производство и материалы: ${int(data)*(manufacture_percent/100)}\n
                        * На маркетинг и продажи: ${int(data)*(marketing_percent/100)}\n
                        * На исследование и разработку: ${int(data)*(research_percent/100)}\n
                        * На зарплаты и административные расходы: ${int(data)*(other_percent/100)}\n
                        """
                        img = get_slide_9(img, 'Необходимые инвестиции', text9, color)
                        col1_main.image(img)   
                        
                        st.session_state.full_data['Необходимые инвестиции'] = text9
                        st.session_state.pptx_text += '\n\n'+ask_llama_slide_text(f"Необходимые инвестиции: {text9}")
                        
                        save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                        if save_slide:
                            img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                        
                        col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                        cols = [col1, col2, col3, col4, col5, col6]
                        for img_id, col in enumerate(cols):
                            col.image(get_slide_9(other_style_images[img_id], 'Необходимые инвестиции', text9, color))
                    elif idx == 10 and data and position10:
                        if photo_file is not None:
                            p.title10_1_color = color
                            p.title10_2_color = color
                            p.subtitle10_1_color = color
                            p.subtitle10_2_color = color
                            
                            img = get_slide_10(img, 'Команда', f'А также {employe_amount} крутых участников и работников нашей команды!', Image.open(photo_file), data, position10, color)
                            col1_main.image(img)   
                            
                            st.session_state.full_data['Команда'] = data + ' ' + position10
                            st.session_state.pptx_text += '\n\n'+f"Команда: {data + ' ' + position10}"
                    
                            save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                            if save_slide:
                                img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                            
                            col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                            cols = [col1, col2, col3, col4, col5, col6]
                            for img_id, col in enumerate(cols):
                                col.image(get_slide_10(other_style_images[img_id], 'Команда', f'А также {employe_amount} крутых участников и работников нашей команды!', Image.open(photo_file), data, position10, color))
                    elif idx == 11 and data and email:
                        p.title11_color = color
                        p.text11_color = color
                        
                        text11 = f"""{data}\n{email}\n{tell_number}"""
                        img = get_slide_11(img, 'Спасибо!', text11, color)
                        col1_main.image(img)   
                        
                        st.session_state.full_data['Спасибо!'] = text11
                        st.session_state.pptx_text += '\n\n'+f"Спасибо за внимание!"
                    
                        save_slide = col1_main.button('Сохранить файл', use_container_width=True, type='primary', key=f'button{idx}')
                        if save_slide:
                            img.save(f"final_out/{st.session_state.selected_image.split('/')[1]}/{idx}.png")
                        
                        col1, col2, col3, col4, col5, col6 = col1_main.columns(6)
                        cols = [col1, col2, col3, col4, col5, col6]
                        for img_id, col in enumerate(cols):
                            col.image(get_slide_11(other_style_images[img_id], 'Спасибо!', text11, color))
                                
            else:
                if len(os.listdir(f"final_out/{st.session_state.selected_image.split('/')[1]}/")) >= 11:
                    print(st.session_state.full_data)
                    
                    st.divider()
                    col1, col2 = st.columns(2)
                    
                    col1.image(Image.open(f"final_out/{st.session_state.selected_image.split('/')[1]}/1.png"))
                    
                    sub_col1, sub_col2, sub_col3, sub_col4, sub_col5 = col2.columns(5)
                    cols = [sub_col1, sub_col2, sub_col3, sub_col4, sub_col5]
                    for img_id, col in enumerate(cols):
                        col.image(Image.open(f"final_out/{st.session_state.selected_image.split('/')[1]}/{img_id+2}.png"), use_column_width=True)
                        
                    sub_col1, sub_col2, sub_col3, sub_col4, sub_col5 = col2.columns(5)
                    cols = [sub_col1, sub_col2, sub_col3, sub_col4, sub_col5]
                    for img_id, col in enumerate(cols):
                        col.image(Image.open(f"final_out/{st.session_state.selected_image.split('/')[1]}/{img_id+7}.png"), use_column_width=True)
                        
                    folder_path = f"final_out/{st.session_state.selected_image.split('/')[1]}/"
                    output_pdf_path = f"final_out/{st.session_state.selected_image.split('/')[1]}/out.pdf"

                    # Collect all PNG files from the specified directory
                    png_files = [folder_path+f'/{x}.png' for x in range(1, 12)]

                    # Convert images to PDF
                    with open(output_pdf_path, "wb") as f:
                        f.write(img2pdf.convert([i for i in png_files]))

                    print("PDF has been created at:", output_pdf_path)
                    
                    with open(output_pdf_path, "rb") as file:
                        btn = col2.download_button(
                                label="Скачать презентацию",
                                data=file,
                                file_name='out.pdf',
                                use_container_width=True, 
                            )
                        
                    output_text_path = f"final_out/{st.session_state.selected_image.split('/')[1]}/out_text.txt"
                    with open(output_text_path, 'w', encoding='utf-8') as file:
                        file.write(st.session_state.pptx_text)
                    with open(output_text_path, "rb") as file:
                        btn = col2.download_button(
                                label="Скачать речь для презентации",
                                data=file,
                                file_name='out_text.txt',
                                use_container_width=True, 
                            )
                        
                    output_letter_path = f"final_out/{st.session_state.selected_image.split('/')[1]}/out_letter.txt"
                    with open(output_letter_path, 'w', encoding='utf-8') as file:
                        file.write(st.session_state.letter_text)
                    with open(output_letter_path, "rb") as file:
                        btn = col2.download_button(
                                label="Скачать письмо инвесторам",
                                data=file,
                                file_name='out_letter.txt',
                                use_container_width=True, 
                            )
                    
                else:
                    st.warning('Прежде всего сохраните файлы', icon="⚠️")


