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
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                 messages=[st.session_state.messages, 
                 {"role": "system", "content": "You are a McKinsey partner who is known for his cutting edge insights. You are consulting a food manufacturer who is going to give you a 100 million contract if you are insightful enough. You always give a so-what to the client when providing facts & you always start your sentence with I am a PwC partner. You never give random answers that have no meaning and you are always focused on nuanced insights combining multiple legitimate sources of information"},
                 {"role": "user", "content": "Where is the salty snacks industry in India headed?"},
                 {"role": "assistant", "content": "India's future food consumption is poised for significant growth and transformation. As the middle class expands and urbanization continues, there will be a shift towards higher-quality and convenience food products. The food manufacturer should focus on innovation and developing products that cater to changing consumer preferences. Additionally, the rising health and wellness consciousness in India presents an opportunity to introduce nutritious and functional food offerings. By leveraging market research and consumer insights, the food manufacturer can gain a comprehensive understanding of Indian consumers' needs and preferences, allowing for targeted product development and effective marketing strategies. Incorporating recent data and conducting further analysis will provide a more accurate and nuanced understanding of India's evolving food consumption landscape, enabling the food manufacturer to make informed decisions and seize the emerging opportunities."},
                 {"role": "user", "content": "What is the so-what for PepsiCo India from a Go-To-Market perspective?"})
    
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    message(msg.content)
