import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

st.set_page_config(page_title='Marketing campaign builder',
                   page_icon=':robot:')
st.header('Marketing campaign builder')

form_input = st.text_area("Enter text", height=275)
task_option = st.selectbox('Please select a taks to be performed?', (
    'Write a sales copy', 'Create a tweet', 'Write a product descrption'), key=1)
age_option = st.selectbox('For which age group?',
                          ('Kid', 'Adult', 'Senior citizen'), key=2)
number_of_words = st.slider("Word limit", 1, 200, 25)
submit = st.button("Generate")


def get_llm_response(user_input, age_option, task_option, number_of_words):
    llm = OpenAI(model='text-davinci-003')
    if age_option == 'Kid':
        examples = [
            {'query': 'What is a mobile?', 'answer': 'A mobile is a magical device that fits in your pocket,like a mini enchanted playground,It has games, videos and much more.'},
            {'query': 'What are your dreams?', 'answer': 'My dreams are like colorfull adventures, where I become a superhero and save the day! I dream of giggles,ice cream parties, and I have a pet dragon named sparcles.'},
        ]
    elif age_option=='Adult':
        examples = [
            {'query': 'What is a mobile?', 'answer': 'A mobile, typically a smartphone, is a portable electronic device that combines various functions, including communication, internet access, apps, and more, allowing users to stay connected and perform tasks on the go.'},
            {'query': 'What is a laptop?', 'answer': 'A laptop is a portable computer that combines a keyboard, screen, and processing power, enabling users to perform various tasks, from work to entertainment, on the go.'},
        ]
    elif age_option=='Senior citizen':
        examples = [
            {'query': 'What is a mobile?', 'answer': 'A mobile is a handy device, like a small computer, that fits in your pocket or purse. It helps make calls, send messages, take pictures, and access the internet, making life more convenient.'},
            {'query': 'What are your laptop?', 'answer': 'A laptop is like a compact, portable computer with a screen and keyboard. It helps you write, browse the internet, and do many tasks, offering flexibility and convenience.'},
        ]
    example_template = """
        Question:{query}
        Response:{answer}
    """
    example_prompt = PromptTemplate(
        input_variables=['query', 'answer'], template=example_template)

    prefix = """You are a {age_option} and {task_option} in less than {word_limit}
        here are some examples:
    """
    suffix = """
    Question:{user_input}
    Response:
    """
    fewshot_prompt = FewShotPromptTemplate(
        prefix=prefix,
        suffix=suffix,
        example_prompt=example_prompt,
        examples=examples,
        input_variables=['user_input', 'age_option', 'task_option','word_limit'],
        example_separator='\n\n'
    )
    return llm(fewshot_prompt.format(user_input=user_input, age_option=age_option, task_option=task_option,word_limit=number_of_words))


if submit:
    response = get_llm_response(user_input=form_input, age_option=age_option,
                                task_option=task_option, number_of_words=number_of_words)

    st.write(response)
