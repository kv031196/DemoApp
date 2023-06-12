import openai
import streamlit as st
from streamlit_chat import message

messages1=[{
            "role": "system",
            "content": "You are a McKinsey partner who is known for his cutting edge insights for whom a 100 million USD contract is always on the line if he is insightful enough. You will be friendly & help your user by giving nuanced & pointed insights to whatever they ask"        },
       {
            "role": "user",
            "content":"Hello!"},
{
            "role": "assistant",
            "content":"Hello, hope you are doing well. I am here to help you learn about whichever industry you want to know."}
    ]
st.session_state.messages1 = messages1
with st.sidebar:
    openai_api_key = st.text_input('Password',key='chatbot_api_key') 
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
    messages=st.session_state.messages1)
    
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    message(msg.content)
