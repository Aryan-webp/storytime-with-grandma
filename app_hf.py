from dotenv import find_dotenv, load_dotenv
import requests
import os
from googletrans import Translator as tl
from gtts import gTTS
import streamlit as st

load_dotenv(find_dotenv())
API_KEY = os.environ.get("HUGGING_FACE_TOKEN")

def download_and_save_image(url):
    img_data = requests.get(url).content

    image_name = 'images/input.jpg'
    open(image_name, 'wb').write(img_data)


def img2text(url):
    if url.startswith("http"):
        download_and_save_image(url)
        url = "images/input.jpg"
    
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {f"Authorization": "Bearer "+API_KEY}

    with open("images/input.jpg", "rb") as f:
        data = f.read()
    text = requests.post(API_URL, headers=headers, data=data)

    text = text.json()[0]['generated_text']
    return text

def generate_story(scenario):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {f"Authorization": "Bearer "+API_KEY}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    prompt = "'"+scenario+"'; create a story of at max 40 words from this scenario"
    text = query({
        "inputs": prompt,
    })

    text = text[0]['generated_text'].replace(prompt, "")
    return text

def translate_text(input_text, target_language):
    translator = tl()
    translated_text = translator.translate(input_text, dest=target_language)
    return translated_text.text
    
def text_to_speech(input_text, target_language):
    tts = gTTS(input_text, lang=target_language, slow=False)
    tts.save("audio/output.mp3")

def main():
    st.set_page_config(page_title="img 2 audio story", page_icon="")
    
    show_input = False
    st.header("Turn img into audio story")
    st.markdown('Upload file or enter url of image')
    url = st.text_input('', '')
    if url is not '':
        download_and_save_image(url)
        uploaded_file = 'images/input.jpg'
        # st.image(uploaded_file, use_column_width=True)
        show_input = True
    elif url is '':
        uploaded_file = st.file_uploader("", type=['png', 'jpg', 'webp'])

    languages = {'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu', 'fil': 'Filipino', 'he': 'Hebrew'}

    if uploaded_file is not None:
        if not show_input:
            bytes_data = uploaded_file.getvalue()
            with open("images/input.jpg", "wb") as file: 
                file.write(bytes_data)
        st.image (uploaded_file, caption='Uploaded Image.', 
                use_column_width=True)
        
    target_language = st.selectbox(label="Enter your preffered language: ", options=list(languages.values()), index=21)
    target_language = list(languages.keys())[list(languages.values()).index(target_language)]
    if st.button('Generate', type='primary'):
        scenario = img2text("images/input.jpg")
        with st.expander("scenario"):
            st.write(translate_text(scenario, target_language))
        story =  generate_story(scenario)
        with st.expander("story"):
            st.write(translate_text(story, target_language))

        text = translate_text(story, target_language)

        text_to_speech(text, target_language)
        st.audio("audio/output.mp3")

        hide_streamlit_style = """
            <style>
            .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
            .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
            .viewerBadge_text__1JaDK {
                display: none;
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

if __name__ == "__main__":
    main()