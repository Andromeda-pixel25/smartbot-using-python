import streamlit as st
import os
import google.generativeai as genai
import speech_recognition as sr
import sounddevice as sd
import pyttsx3 as engine

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
 
def listen():
   recognizer = sr.Recognizer()
   input_devices = list_input_devices()
   if not input_devices:
        st.error("No input devices (microphones) found. Please connect a microphone.")
        return None  # Skip listening if no devices are found
   st.write("Available input devices:")
   st.write(input_devices)
   with sr.Microphone() as source:
      st.info("Listening.....")
      try:
         audio=recognizer.listen(source,timeout=5) #listen to input with 5sec timeout
         command=recognizer.recognize_google(audio)
         st.success(f"recognized: {command}")
         return command
      except sr.UnknownValueError:
         st.error("Sorry, I couldn't understand that.")
         return None
      except sr.RequestError:
          st.error("Voice recognition service is unavailable.")
          return None 
      except OSError as e:
        # Handle case where no input device is available
        st.error(f"Error: {e}. No microphone detected or available.")
        return None
      
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

  
prompt_text=st.chat_input("ask away..")
voice_button=st.button("voice")

if voice_button:
  prompt_voice=listen()
else:
   prompt_voice=None


          
if prompt_text:
  st.chat_message("user").markdown(prompt_text)
  response = st.session_state.messages.send_message(prompt_text) 
  with st.chat_message("assistant"):
      st.markdown(response.text)
      
elif prompt_voice:
   st.chat_message("user").markdown(prompt_voice)
   response = st.session_state.messages.send_message(prompt_voice)
   with st.chat_message("assistant"):
      st.markdown(response.text)
      speak(response.text) 


