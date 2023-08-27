from gradio_client import Client
from googletrans import Translator
from positions import positions as p
import streamlit as st


translator = Translator()

@st.cache_data(show_spinner=False)
def get_translation(text, dest='en'):
    return translator.translate(text, dest=dest).text

@st.cache_data(show_spinner=False)
def shorten_text(text, max_length):
    # If the text is already shorter than or equal to the max_length, return it as is
    if len(text) <= max_length:
        return text

    # Split the text into sentences
    sentences = text.split(". ")
    
    # Iteratively append sentences to the shortened text until the max_length is reached
    shortened_text = ""
    for sentence in sentences:
        if len(shortened_text + sentence) + 1 <= max_length:  # +1 for the period
            shortened_text += sentence + ". "
        else:
            break

    # Return the shortened text without the trailing space
    return shortened_text.strip()


@st.cache_data()
def ask_llama_slide2(prompt):
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")

    result = client.predict(
                    f"""'{get_translation(prompt)}' - write paragraph about the problem; return only asked text without special tokens, quotes and info about number of chars""",	
                    api_name="/chat"
    )
    result = get_translation(result, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').split('(')[0]
    return shorten_text(result, p.text2_max_symbols)


@st.cache_data()
def ask_llama_slide3(prompt):
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")

    result = client.predict(
                    f"""write two paragraphs('our startup idea', 'what we want to do') based on this - '{get_translation(prompt)}' - return only text without special tokens, quotes and info about number of chars""",	
                    api_name="/chat"
    )
    result1, result2 = get_translation(result, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').split('(')[0].split('\n\n')
    result1, result2 = shorten_text(result1, p.text3_1_max_symbols), shorten_text(result2, p.text3_2_max_symbols)
    return result1, result2


@st.cache_data()
def ask_llama_slide4(prompt):
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
    result = client.predict(
                    f"""return only asked text; write three paragraphs(split the solution idea) based on this - '{get_translation(prompt)}' - return only asked text without special tokens, emojies, quotes and info about number of chars""",	
                    api_name="/chat"
    )
    result1, result2, result3 = get_translation(result, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').replace('Конечно, вот три абзаца, основанные на данной идее решения:\n\n', '').split('(')[0].split('\n\n')
    result1, result2, result3 = shorten_text(result1, p.text4_1_max_symbols), shorten_text(result2, p.text4_2_max_symbols), shorten_text(result3, p.text4_3_max_symbols)
    
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
    subtitle1 = client.predict(
                    f"""write 2-words title based on this - '{get_translation(result1)}'""",	
                    api_name="/chat"
    )
    subtitle1 = get_translation(subtitle1, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').split('(')[0].split('\n\n')[0]

    subtitle2 = client.predict(
                    f"""write 2-words title based on this - '{get_translation(result2)}'""",	
                    api_name="/chat"
    )
    subtitle2 = get_translation(subtitle2, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').split('(')[0].split('\n\n')[0]

    subtitle3 = client.predict(
                    f"""write 2-words title based on this - '{get_translation(result3)}'""",	
                    api_name="/chat"
    )
    subtitle3 = get_translation(subtitle3, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').split('(')[0].split('\n\n')[0]
    
    return result1, result2, result3, subtitle1, subtitle2, subtitle3


@st.cache_data()
def ask_llama_slide5(prompt):
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
    result = client.predict(
                    f"""return only asked text; write three paragraphs based on this and try to convince that it's important, but don't use any numbers- '{get_translation(prompt)}' - return only asked text without special tokens, emojies, quotes and info about number of chars""",	
                    api_name="/chat"
    )
    result1, _, _ = get_translation(result, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').replace('Конечно, вот три абзаца, основанные на данной идее решения:\n\n', '').split('(')[0].split('\n\n')
    result1 = shorten_text(result1, 400)

    return result1


@st.cache_data()
def ask_llama_slide6(prompt):
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
    result = client.predict(
                    f"""return only asked text;  tell why it is important, please use all numbers- '{get_translation(prompt)}' - return only asked text without special tokens, emojies, quotes and info about number of chars""",	
                    api_name="/chat"
    )
    result = ' '.join([x for x in get_translation(result, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').replace('Конечно, вот запрошенная информация:', '').split('(')[0].replace('\n', ' ').split() if len(x) > 0])
    return result


@st.cache_data()
def ask_llama_slide7(prompt):
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
    result = client.predict(
                    f"""return only asked text; write a paragraph about your competitive advantages based on this text, but note that it is your startup - '{get_translation(prompt)}' - return only asked text without special tokens, emojies, quotes and info about number of chars""",	
                    api_name="/chat"
    )
    result = get_translation(result, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').split('(')[0].replace('\n\n', ' ')
    result = result[result.index(':')+2:]
    return shorten_text(result, 550)


@st.cache_data()
def ask_llama_slide8(prompt):
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
    result = client.predict(
                    f"""return only asked text; write a paragraph about your business model and pricing based on this text, but note that it is your startup and dont use the name in text - '{get_translation(prompt)}' - return only asked text without special tokens, emojies, quotes and info about number of chars""",	
                    api_name="/chat"
    )
    result = get_translation(result, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').split('(')[0].replace('\n\n', ' ')
    result = result[result.index(':')+2:]
    return shorten_text(result, 550)


@st.cache_data()
def ask_llama_slide_text(prompt):
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
    result = client.predict(
    				f"""return only asked text; write a beautiful wondeful speech for the slide text from presentation, but dont greet - '{get_translation(prompt)}' - return only asked text without special tokens, emojies, quotes and info about number of chars""",	
    				api_name="/chat"
    )
    result = get_translation(result, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').replace('"', '').split('(')[0].replace('\n\n', ' ')
    result = result[result.index(':')+2:].replace('Дамы и господа, ', '')

    return result


def ask_llama_assist(prompt, base_text):
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
    result = client.predict(
				f"""return only asked text; please, {get_translation(prompt)} this text: - '{get_translation(base_text)}' - return only asked text without special tokens, emojies, quotes and info about number of chars""",	
				api_name="/chat"
    )
    result = get_translation(result, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').split('(')[0].replace('\n\n', ' ')
    try:
        result = result[result.index(':')+2:].replace('\'', ' ').replace('\"', ' ')
    except:
        result = result.replace('\'', ' ').replace('\"', ' ')
    return result


def make_letter_for_investor(query):
    client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
    result = client.predict(
				f"""return only 
    asked text; Please write a letter to the investor to take money on your startup with this description: '{get_translation(query)}' - return only asked text without special tokens, emojies, quotes and info about number of chars""",	
				api_name="/chat"
    )
    result = ' '.join([x for x in get_translation(result, dest='ru').replace('«', '').replace('»', '').replace('</s>', '').replace('Конечно, вот запрошенная информация:', '').split('(')[0].replace('\n', ' ').split() if len(x) > 0])
    return result.replace('Уважаемый [Имя инвестора]', 'Здравствуйте')