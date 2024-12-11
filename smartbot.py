import streamlit as st
import os
import google.generativeai as genai
import pyttsx3 as engine
from streamlit_mic_recorder import mic_recorder, speech_to_text
from audio_recorder_streamlit import audio_recorder
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch

genai.configure(api_key="AIzaSyA7V6N800cWrvaW2hlgHazi62i4Gh-idZk")
model = genai.GenerativeModel('gemini-pro')

# Initialize the text-to-image model (Stable Diffusion)
@st.cache_resource
def load_stable_diffusion_model():
    # Load the Stable Diffusion pipeline (this requires a GPU for faster inference)
    stable_diffusion_model = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float32)
    stable_diffusion_model.to("cuda" if torch.cuda.is_available() else "cpu")
    return stable_diffusion_model

# Initialize chat session
messages = model.start_chat()

# Load Stable Diffusion model
stable_diffusion_model = load_stable_diffusion_model()

st.title("ZypherAi")
st.markdown("_________________________________________________________________________________")
st.markdown("Powered by Google Generative AI for Seamless Conversations")
image = "https://github.com/Andromeda-pixel25/smartbot-using-python/blob/main/letter-z%20(1).png?raw=true"
st.logo(image)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Initialize messages in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = model.start_chat(history=[])

# Display chat history
for message in st.session_state.messages.history:
    role = role_to_streamlit(getattr(message, "role"))
    text = ""
    parts = getattr(message, "parts", None)
    if parts:
        for part in parts:
            if hasattr(part, "text"):
                text = part.text
                break
    with st.chat_message(role):
        st.markdown(text)

# Handle user input
prompt_text = st.chat_input("Ask away...")
gen_image = st.button("Generate image")

# Create a container for the microphone and audio recording
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

# Handle text input
if prompt_text:
    st.chat_message("user").markdown(prompt_text)
    response = st.session_state.messages.send_message(prompt_text)
    with st.chat_message("assistant"):
        st.markdown(response.text)

# For voice input      
if audio_bytes:
    with st.spinner("Transcribing..."):
        # Write the audio bytes to a temporary file
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        # Convert the audio to text using the speech_to_text function
        transcript = speech_to_text(webm_file_path)
        if transcript:
            # Send the transcribed text to the chat model
            response = st.session_state.messages.send_message(transcript)
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)   

            with st.chat_message("assistant"):
                st.markdown(response.text)
            speak(response.text)
        else:
            st.error("Could not transcribe the audio. Please try again.")

# For image generation
if gen_image:
    prompt_text = st.chat_input("Enter a description to generate an image:")
    st.write(prompt_text)
    if prompt_text:
        try:
            # Generate an image based on the text input
            with st.spinner("Generating image..."):
                image_gen = stable_diffusion_model(prompt=prompt_text)
                if image_gen and len(image_gen.images) > 0:
                    image = image_gen.images[0]
                    st.image(image, caption='Generated Image', use_column_width=True)
        except Exception as e:
            st.error(f"Error generating image: {e}")
