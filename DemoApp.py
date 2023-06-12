import openai
import streamlit as st
from streamlit_chat import message

with st.sidebar:
    openai_api_key = st.text_input('OpenAI API Key',key='chatbot_api_key') 
st.title("🧠 Insight Generation Platform")
