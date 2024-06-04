# storytime-with-grandma

### Ever heard the proverb "Every picture tells it's story" ? Well, now you've heard and there is something else that you can hear; the story of the image. For the technical aspect, this project takes an image as input an uses the image captioning model 'Blip' to caption it. This caption is passed to a LLM named 'Mixtral-8x7B' which generates a 30 word story. This story is then translated to the desired language and this story is converted to an audio file which can be played by the user. Click the link below to take a sneak peek.

## [grandma.streamlit.app](https://grandma.streamlit.app/)


## Also, you can run this locally by following this steps:
### 1. Clone this repository
```
git clone https://github.com/Aryan-webp/storytime-with-grandma
cd storytime-with-grandma
```

### 2. Install the dependencies
```
pip install -r requirements.txt
```

### 3. Enter your credentials
#### Visit [huggingface.co](https://huggingface.co) and log in to your account or create a new one.
#### Then, create a new api token by visiting [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
#### Copy this api token and make sure to keep it private
#### Now, open .env file and replace ```'YOUR_API_TOKEN_HERE'``` with your huggingface api token.


### 4. Now that everything is ready, let's run the app
#### a. If you have a dedicated GPU and a fast internet connection, use this as it utilizes a lot of processing power and bandwidth because it downloads all the models and runs them.
```
streamlit run app.py
```

#### b. If you don't have a dedicated GPU, use this
```
streamlit run app_hf.py
```
