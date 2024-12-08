import streamlit as st
import os
import google.generativeai as genai
from gtts import gTTS
import playsound
from streamlit_mic_recorder import mic_recorder  # Assuming you're still using streamlit_mic_recorder

# Set up the Google Generative AI API
genai.configure(api_key="AIzaSyA7V6N800cWrvaW2hlgHazi62i4Gh-idZk")
model = genai.GenerativeModel('gemini-pro')

# Initialize chat history
messages = model.start_chat()

# Function to speak text using Google TTS and playsound
def speak(text):
    tts = gTTS(text)
    tts.save("output.mp3")  # Save the speech as an MP3 file
    playsound.playsound("output.mp3")  # Play the MP3 file

# Streamlit UI
st.title("ZypherAi")
st.markdown("_________________________________________________________________________________")
st.markdown("Powered by Google Generative AI for Seamless Conversations")
image="https://github.com/Andromeda-pixel25/smartbot-using-python/blob/main/letter-z%20(1).png?raw=true"
st.logo(image)

# Function to handle input and send it to the AI model
def handle_input():
    # Get text input from the user
    prompt_text = st.chat_input("Ask away...")
    
    if prompt_text:
        st.chat_message("user").markdown(prompt_text)
        # Send the text input to the Google Generative AI model
        response = st.session_state.messages.send_message(prompt_text)
        with st.chat_message("assistant"):
            st.markdown(response.text)
            speak(response.text)  # Convert the response to speech

    # Handle voice input
    voice_button = st.button("Voice Input")
    if voice_button:
        audio_data = mic_recorder()
        if audio_data is not None and hasattr(audio_data, 'text'):
            prompt_voice = audio_data.text
            st.chat_message("user").markdown(prompt_voice)
            response = st.session_state.messages.send_message(prompt_voice)
            with st.chat_message("assistant"):
                st.markdown(response.text)
                speak(response.text)

# Ensure chat history is stored correctly
if "messages" not in st.session_state:
    st.session_state.messages = model.start_chat(history=[])

# Display chat history
for message in st.session_state.messages.history:
    role = "assistant" if getattr(message, "role") == "model" else "user"
    text = ""
    parts = getattr(message, "parts", None)
    if parts:
        for part in parts:
            if hasattr(part, "text"):
                text = part.text
                break
    with st.chat_message(role):
        st.markdown(text)

# Handle user input and responses
handle_input()
       


