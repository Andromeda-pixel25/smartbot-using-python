import streamlit as st
import os
import google.generativeai as genai
import sounddevice as sd
import pyttsx3 as engine
from streamlit_mic_recorder import mic_recorder, speech_to_text
from audio_recorder_streamlit import audio_recorder

genai.configure(api_key="AIzaSyA7V6N800cWrvaW2hlgHazi62i4Gh-idZk")
model = genai.GenerativeModel('gemini-pro')

messages = model.start_chat()

st.title("ZypherAi")
st.markdown("_________________________________________________________________________________")
st.markdown("Powered by Google Generative AI for Seamless Conversations")
image="https://github.com/Andromeda-pixel25/smartbot-using-python/blob/main/letter-z%20(1).png?raw=true"
st.logo(image)


def list_input_devices():
    try:
        devices = sd.query_devices()
        input_devices = [device for device in devices if device['max_input_channels'] > 0]
        return input_devices
    except Exception as e:
        st.error(f"Error detecting input devices: {e}")
        return []
 

def speak(text):
   engine.say(text)
   engine.runAndWait()

def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

if "messages" not in st.session_state:
    st.session_state.messages = model.start_chat(history = [])

 
for message in st.session_state.messages.history:
  role = role_to_streamlit(getattr(message, "role"))
  text = ""
  parts = getattr(message, "parts", None) #none is specified to run even if nothing exists
  if parts:
    for part in parts:  
      if hasattr(part, "text"):  # Check if `text` attribute exists
          text = part.text
          break  

        # display the history
  with st.chat_message(role):
    st.markdown(text)

prompt_text=st.chat_input("Ask away...")

# Create a container for the microphone and audio recording
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

if prompt_text:
  st.chat_message("user").markdown(prompt_text)
  response = st.session_state.messages.send_message(prompt_text) 
  with st.chat_message("assistant"):
      st.markdown(response.text)
#for voice input      
if audio_bytes:
    with st.spinner("Transcribing..."):
        # Write the audio bytes to a temporary file
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        # Convert the audio to text using the speech_to_text function
        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)   

            response=st.session_state.messages.send_message(transcript)
            with st.chat_message("assistant"):
               st.markdown(response.text)
            speak(response.text)
        else:
           st.error("Could not transcribe the audio. Please try again.")
       


