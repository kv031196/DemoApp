import openai
import streamlit as st
from streamlit_chat import message

with st.sidebar:
    openai_api_key = st.text_input('OpenAI API Key',key='chatbot_api_key') 
st.title("🧠 Insight Generation Platform")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! What piques your curiosity today?"}]
with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    user_input = a.text_input(
        label="Your message:",
        placeholder="What would you like to know?",
        label_visibility="collapsed",
    )
    b.form_submit_button("Send", use_container_width=True)
    
for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")

if user_input and not openai_api_key:
    st.info("Please add the key given by Karanveer to continue.")
if user_input and openai_api_key:
    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{
            "role": "system",
            "content": "You are a McKinsey partner who is known for his cutting edge insights. You are consulting a food manufacturer who is going to give you a 100 million contract if you are insightful enough. You always give a so-what to the client when providing facts. You never give random answers that have no meaning and you are always focused on nuanced insights combining multiple legitimate sources of information. You also never use can & always are more affirmative and say should",
        },
       ],
)
    
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    message(msg.content)
