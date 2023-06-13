import langchain
import llama_index
import openai
import streamlit as st
from streamlit_chat import message

model="gpt-3.5-turbo"
def get_initial_message():
    messages=[
            {"role": "system", "content": "You are a McKinsey consulting Partner who is known for his cutting edge insights. Every answer you give is nuanced & full of insights. Your responses are always structured, MECE & are written with the aim that a client would be so impressed by them that they'll offer a 100 million USD contract."},
            {"role": "user", "content": "I want to learn how to understand industries"},
            {"role": "assistant", "content": "Certainly, what do you want to know, the market, the competition or customers?"}
        ]
    return messages

def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
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
    response = get_chatgpt_response(messages,model)
    messages = update_chat(messages, "assistant", response)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)
        
if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        st.write(messages)
