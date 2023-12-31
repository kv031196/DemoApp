import langchain
import llama_index
import openai
import streamlit as st
from streamlit_chat import message

model="gpt-3.5-turbo"
temperature=1
top_p=0.5
frequency_penalty=0.5

def get_initial_message():
    messages=[
            {"role": "system", "content": "You are a McKinsey consulting Partner who is known for his detailed, exhaustive & cutting-edge insights. Every answer you give covers all aspects, is nuanced & full of insights. Your responses are always bulleted, structured, MECE & always have strategic, actionable implications for your client. The aim of the answers is always to impress a client so that they  would be so impressed by them that they'll offer a 100 million USD contract. More importantly anything you say is backed with data & sources"},
            {"role": "system", "content": "You will additionally end every response with a source mentioning it"},
            {"role": "user", "content": "I want to learn about the salty snacks industry"},
            {"role": "assistant", "content": "Certainly, what do you want to know? the market & its future, the competition & their dynamics or customers & their changes in preferences? Or do you want to understand the strategies that you should undertake to win in this sector?"}
        ]
    return messages

def get_chatgpt_response(messages, model="gpt-3.5-turbo",temperature=1,top_p=0.5,frequency_penalty=0.5):
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages, 
    temperature=temperature,
    top_p=top_p,
    frequency_penalty=frequency_penalty
    
    )
    return  response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

with st.sidebar:
    openai_api_key = st.text_input('Password',key='chatbot_api_key') 
st.title("🧠 Insight Generation Platform")
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
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
    messages = st.session_state['messages']
    messages = update_chat(messages, "user", user_input)
    # st.write("Before  making the API call")
    # st.write(messages)
    response = get_chatgpt_response(messages,model,temperature, top_p,frequency_penalty)
    messages = update_chat(messages, "assistant", response)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)
        
if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        st.write(messages)
