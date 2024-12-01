# smartbot-using-python
This repository features a fully interactive AI Chatbot using Streamlit for the frontend and Google Generative AI (e.g., Gemini API) for the backend. The chatbot offers a scalable, modern solution for applications like customer support, virtual assistants, and educational tools.


Features
Interactive UI with Streamlit:

A user-friendly web interface for engaging with the chatbot.
Streamlit's chat_message feature for a chat-like display.
Supports both text-based input and response visualization.
Generative AI with Google APIs:

Powered by Google Generative AI for high-quality, contextual, and human-like responses.
Implements secure API integration using the google.generativeai Python library.
Session Management:

Maintains conversation history across sessions for a seamless user experience.
Dynamically updates the chat interface with user inputs and AI responses.
Customizable Roles:

Distinction between "user" and "assistant" roles for clear conversational flow.
Flexible backend for adding system-level prompts or context.
Lightweight Deployment:

Easily deployable on platforms like Streamlit Cloud, Heroku, or any server supporting Python.
Getting Started
Prerequisites
Python 3.8+
Google Cloud API Key
Generate an API key for accessing Google Generative AI via the Google Cloud Console.
Dependencies
Install the required libraries using pip.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/ai-chatbot-streamlit-googleai.git
cd ai-chatbot-streamlit-googleai
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Up API Key:

Replace YOUR_API_KEY in the main.py file with your Google API key:
python
Copy code
genai.configure(api_key="YOUR_API_KEY")
Run the Application:

bash
Copy code
streamlit run main.py
Access the Chatbot:

Open your browser and go to http://localhost:8501.
Repository Structure
bash
Copy code
ai-chatbot-streamlit-googleai/
├── main.py                 # Main application script
├── requirements.txt        # Python dependencies
├── README.md               # Repository documentation
├── LICENSE                 # Project license
├── assets/                 # Images or UI assets (optional)
└── utils/                  # Utility functions for chatbot extensions
How It Works
Backend:

The chatbot utilizes the Google Generative AI API to generate responses to user inputs.
Context-aware responses are managed via the google.generativeai.GenerativeModel.
Frontend:

The Streamlit interface offers real-time interactions.
The st.chat_message feature creates a conversational view.
Session State:

Utilizes Streamlit's session_state to maintain chat history during the session.
Customization
Change Default Prompts:

Add initial system-level prompts to guide the chatbot's behavior:
python
Copy code
messages = model.start_chat(history=[{"role": "system", "content": "You are a helpful assistant."}])
Modify the UI:

Customize colors, fonts, or styles in the main.py using Streamlit's theming options.
Extend Functionality:

Add features like file uploads, multi-language support, or even custom APIs for specific tasks.
Example Usage
Ask a Question:

Type a question in the input box and press Enter.
Example: "What's the weather like today?"
Receive a Response:

The chatbot will generate a human-like response using Google Generative AI.
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch for your feature/bugfix.
Submit a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgments
Google Generative AI for the backend conversational intelligence.
Streamlit for the intuitive frontend framework.
