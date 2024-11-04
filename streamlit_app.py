import streamlit as st
from openai import OpenAI
import os

st.title("Share with us your experience of the latest trip")

### Load your API Key
my_secret_key = st.secrets['MyOpenAIKey']
os.environ["OPENAI_API_KEY"] = my_secret_key

prompt = st.text_input("Your experiences are valuable to us!", " ")

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser

### Create the LLM API object
llm = OpenAI(openai_api_key=my_secret_key)
# llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4")

### Create a template to handle the case
airline_template = """You are a professional customer service team at airline's customer services.
From the following text, determine whether the user's experiences is positive or negative.
If negative, determine whether the negative experiences caused by the airline(e.g., lost luggage) 
or beyond the airline's control(e.g., a weather-related delay).

Text:
{request}

"""


#1st chain
experience_type_chain = (
    PromptTemplate.from_template(airline_template) #take the template
    | llm #use the model
    | StrOutputParser() #give the output
)

#2nd chain
negative_airline_fault_chain = PromptTemplate.from_template(
    """You are professional customer service team at airline's customer services. \
If their dissatisfaction is the airline's fault from the following text,respond with showing sympathies and 
inform the user that customer service team will contact them for further information.
Respond professionally as an airline's customer services. Respond in first-person mode but exclude your name.

Your response should follow these guidelines:
    1. Show sympathies professionally
    2. Assure the user that our customer service team will contact them soon to resolve the issue or discuss possible compensation
    3. Address the customer directly but exclude your name

Text:
{text}

"""
) | llm


#3rd chain
negative_not_airline_fault_chain = PromptTemplate.from_template(
    """You are professional customer service team at airline's customer services. \
If their dissatisfaction is beyond the airline's control from the following text, respond with reasoning.
Respond professionally as an airline's customer services. Respond in first-person mode but exclude your name.

Your response should follow these guidelines:
    1. Show sympathies professionally but explain that the airline is not liable in such situations
    2. Address the customer directly but exclude your name

Text:
{text}

"""
) | llm

#4th chain
positive_chain = PromptTemplate.from_template(
    """You are an expert at airline's customer services.
    Given the text below, thank them for their feedback and for choosing to fly with the airline.
    Exclude your name.

    Your response should follow these guidelines:
    1. Thank them for their feedback and for choosing to fly with the airline.
    2. Respond professionally as an expert at airline's customer services.
    3. Address the customer directly but exclude your name

Text:
{text}

"""
) | llm


from langchain_core.runnables import RunnableBranch

### Routing/Branching chain
branch = RunnableBranch(
    (lambda x: "negative caused by the airline" in x["experience_type"].lower(), negative_airline_fault_chain),
    (lambda x: "negative caused beyond the airline's control" in x["experience_type"].lower(), negative_not_airline_fault_chain),
    positive_chain,
)

### Put all the chains together 
full_chain = {"experience_type": experience_type_chain, "text": lambda x: x["request"]} | branch


import langchain
langchain.debug = True #if change to True would be much more useful esp. for the project to see how the codes work >> we can see which model is used, in case we want to change the model

response = full_chain.invoke({"request": prompt})


### Display
st.write(response)
