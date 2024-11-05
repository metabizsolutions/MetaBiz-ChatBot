import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if you have one
load_dotenv()

# Load API key from environment variable
gemini_api_key = os.environ.get("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=gemini_api_key)

def get_gemini_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "An error occurred. Please try again later."

def main():
    st.set_page_config(page_title="MetaBiz Chatbot", page_icon="🤖", layout="wide")
    
    # Centered Title
    st.markdown("<h1 style='text-align: center;'>MetaBiz Chatbot</h1>", unsafe_allow_html=True)

    # Initialize session state for messages if it doesn't exist
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages in a styled container with scrolling
    chat_container = st.container()
    with chat_container:
        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Use the chat input for user messages
    prompt = st.chat_input("Say something")
    if prompt:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate the bot's response
        with st.spinner("Generating response..."):
            response = get_gemini_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})

            with st.chat_message("assistant"):
                st.markdown(response)

    # Add a footer or any other component below the input box
    st.markdown(
        "<div style='text-align: center; margin-top: 20px;'><small>Powered by MetaBiz AI 🤖</small></div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
