import os
import streamlit as st
from langchain.llms import OpenAI
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

def fetch_answer(question):
    llm = OpenAI(model='text-davinci-003',temperature=0)
    answer = llm(question)
    return answer


st.set_page_config(page_title='Quesiton Answer bot',page_icon=':robot:')
st.header('Quesiton Answer bot')

def get_text():
    input_text = st.text_input("You:",key='input')
    return input_text

user_input = get_text()
response = fetch_answer(user_input)
submit = st.button("generate")

if submit:
    st.subheader("Answer:")
    st.write(response)