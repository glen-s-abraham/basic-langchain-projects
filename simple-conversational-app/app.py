import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


st.set_page_config(page_title='Simple chat bot', page_icon=':robot:')
st.header('Simple chat bot')

if 'messages' not in st.session_state:
    st.session_state.messages = [SystemMessage(
        content='You are a sarcastic AI assistant')]


def load_answer(question):
    chat = ChatOpenAI(temperature=.7, model='gpt-3.5-turbo')
    st.session_state.messages.append(HumanMessage(content=question))
    answer = chat(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=answer.content))
    return answer.content


def get_text():
    input_text = st.text_input("You:", key='input')
    return input_text


user_input = get_text()
response = load_answer(user_input)
submit = st.button("generate")

if submit:
    st.subheader("Answer:")
    st.write(response)
