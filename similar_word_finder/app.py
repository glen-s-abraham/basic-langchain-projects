import os
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import CSVLoader
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

st.set_page_config(page_title='Similar word finder', page_icon=':robot:')
st.header('Similar word finder')

embeddings = OpenAIEmbeddings()
loader = CSVLoader(file_path='./wordData.csv', csv_args={
    'delimiter': ',',
    'quotechar': '"',
    'fieldnames': ['Words']
})

data = loader.load()

print(data)

db = FAISS.from_documents(data, embeddings)


def get_text():
    input_text = st.text_input("You:", key='input')
    return input_text


user_input = get_text()
submit = st.button("Find similar things")

if submit:
    docs = db.similarity_search(user_input)
    st.subheader("Answer:")
    st.text(docs[0].page_content)
    st.text(docs[1].page_content)
