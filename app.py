from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
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
    
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large", max_new_tokens=256)

    text = image_to_text(url)[0]['generated_text']
    print("Scenario: ",text)
    return text

def generate_story(scenario):
    text_gen = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2", max_new_tokens=256)

    prompt = "'"+scenario+"'; create a story from this scenario"
    text = text_gen(prompt)
    text = text[0]['generated_text'].replace(prompt, "")

    print("Story: ",text)
    return text

def translate_text(input_text, target_language):
    translator = tl()
    translated_text = translator.translate(input_text, dest=target_language)
    print("Translated story: ",translated_text.text)
    return translated_text.text
    
def text_to_speech(input_text, target_language):
    tts = gTTS(input_text, lang=target_language, slow=False)
    tts.save("audio/output.mp3")

def main():
    st.set_page_config(page_title="img 2 audio story", page_icon="")
    
    st.header("Turn img into audio story")
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")
    
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open(uploaded_file.name, "wb") as file: 
            file.write(bytes_data)
        st.image (uploaded_file, caption='Uploaded Image.', 
                use_column_width=True)
        scenario = img2text (uploaded_file.name)
        story =  generate_story(scenario)
        text_to_speech(story, 'en')

        with st.expander("scenario"):
            st.write(scenario)
        with st.expander("story"):
            st.write(story)

        st.audio("audio/output.mp3")

if __name__ == "__main__":
    main()