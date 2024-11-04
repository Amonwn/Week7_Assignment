import streamlit as st
from openai import OpenAI
import os

st.title("Share with us your experience of the latest trip")

### Load your API Key
my_secret_key = st.secrets['MyOpenAIKey']
os.environ["OPENAI_API_KEY"] = my_secret_key

prompt = st.text_input("We want to hear from you!", " ")

from langchain.llms import OpenAI
from langchain_core.output_parsers import StrOutputParser


### Create the LLM API object
llm = OpenAI(openai_api_key=my_secret_key, model="gpt-4o-mini")
# llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4")

### Create a template to handle the case
airline_template = """You are an expert at airline's customer services.
From the following text, determine whether the user's experiences is positive or negative.

Text:
{request}

"""

#1st chain
experience_type_chain = (
    PromptTemplate.from_template(airline_template) #take the template
    | llm #use the model
    | StrOutputParser() #give the output
)

