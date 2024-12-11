import streamlit as st
import pyttsx3 as engine
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import os
import google.generativeai as genai

# Initialize Google AI API
genai.configure(api_key="AIzaSyA7V6N800cWrvaW2hlgHazi62i4Gh-idZk")
model = genai.GenerativeModel('gemini-pro')

# Initialize pyttsx3 for text-to-speech
engine.init()
def list_microphones():
    mic_list = sr.Microphone.list_microphone_names()
    print("Available Microphones:", mic_list)
    return mic_list

mic_list = list_microphones()
if not mic_list:
    print("No microphones found!")
    
# Function to handle speaking text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to handle speech recognition
def listen_to_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            st.success(f"Recognized: {command}")
            return command
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            st.error("Voice recognition service is unavailable.")
            return None

# Function to handle the conversation and append messages
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Streamlit UI layout
st.title("ZypherAi")
st.markdown("_________________________________________________________________________________")
st.markdown("Powered by Google Generative AI for Seamless Conversations")
image="https://github.com/Andromeda-pixel25/smartbot-using-python/blob/main/letter-z%20(1).png?raw=true"
st.logo(image)

# Start chat if not already in session state
if "messages" not in st.session_state:
    st.session_state.messages = model.start_chat(history=[])

# Display the chat history
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

# Create a container for the input and microphone button
col1, col2 = st.columns([8, 1])  # 8 parts for input, 1 part for microphone button

with col1:
    # Input text field
    prompt_text = st.text_input("Ask away...")

with col2:
    # Mic button to activate voice input
    mic_button = st.button("🎤")  # 🎤 is the mic icon

# Handle text input
if prompt_text:
    st.chat_message("user").markdown(prompt_text)
    response = st.session_state.messages.send_message(prompt_text)
    with st.chat_message("assistant"):
        st.markdown(response.text)

# Handle voice input
elif mic_button:
    voice_input = listen_to_audio()
    if voice_input:
        st.chat_message("user").markdown(voice_input)
        response = st.session_state.messages.send_message(voice_input)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        speak(response.text)

