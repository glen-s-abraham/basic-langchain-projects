from streamlit_chat import message
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

st.session_state.conversation = ConversationChain(
    llm=OpenAI(),
    verbose=True,
    memory=ConversationBufferMemory()
)


def get_response(user_input):
    return st.session_state.conversation.run(user_input)


st.set_page_config(page_title='Chat-Gpt-Clone',
                   page_icon=':robot:')
st.markdown("<h1 style='text-align: center'>How can I help you?</h1>",
            unsafe_allow_html=True)

with st.sidebar:
    summarize_button = st.sidebar.button(
        'Summarize the conversation', key='summary')
    if summarize_button:
        summarize_placeholder = st.sidebar.write(
            "Nice chatting with you :\n\n"+st.session_state['conversation'].memory.buffer)


container = st.container()
response_container = st.container()


with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area(
            "Your question goes here:", key='input', height=100)
        submit_button = st.form_submit_button(label='send')
        if submit_button:
            st.session_state['messages'].append(user_input)
            res = get_response(user_input)
            st.session_state['messages'].append(res)
            
            with response_container:
                for i,msg in enumerate(st.session_state['messages']):
                    if i%2 ==0:
                        message(msg,is_user=True,key=f'{i}_user')
                    else:
                        message(msg,is_user=False,key=f'{i}_bot')