import streamlit as st
from openai import OpenAI
import os

st.title("Share with us your experience of the latest trip")

### Load your API Key
my_secret_key = st.secrets['MyOpenAIKey']
os.environ["OPENAI_API_KEY"] = my_secret_key

prompt = st.text_input("We want to hear from you!", " ")

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser


### Create the LLM API object
llm = OpenAI(openai_api_key=my_secret_key, model="gpt-4o-mini")
# llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4")

### Create a template to handle the case
airline_template = """You are an expert at airline's customer services.
From the following text, determine whether the user's experiences is positive or negative.
If negative, determine whether the negarive experiences caused by the airline(e.g., lost luggage) 
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
    """You are an expert at airline's customer services. \
Determine the cause of their dissatisfaction is the airline's fault or beyond the airline's control from the following text.
Respond with reasoning. Respond professionally as an airline's customer services. Respond in first-person mode.

Your response should follow these guidelines:
    1. Show sympathies professionally and inform the user that customer service will contact them soon
    2. Address the customer directly

Text:
{text}

"""
) | llm


#3rd chain
negative_not_airline_fault_chain = PromptTemplate.from_template(
    """You are an expert at airline's customer services. \
Determine the cause of their dissatisfaction is the airline's fault or beyond the airline's control from the following text.
Respond with reasoning. Respond professionally as an airline's customer services. Respond in first-person mode.

Your response should follow these guidelines:
    1. Show sympathies professionally but explain that the airline is not liable in such situations
    2. Address the customer directly

Text:
{text}

"""
) | llm


