import streamlit as st
from openai import OpenAI
import os

st.title("Share with us your experience of the latest trip")

### Load your API Key
my_secret_key = st.secrets['MyOpenAIKey']
os.environ["OPENAI_API_KEY"] = my_secret_key

prompt = st.text_input("We want to hear from you!", " ")

"""
### OpenAI model
client = OpenAI()
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "Complete the following prefix"},
    {"role": "user", "content": prompt}
  ],
)

### Display
st.write(
    response.choices[0].message.content
)
"""

from langchain.llms import OpenAI
from langchain_core.output_parsers import StrOutputParser


### Create the LLM API object
llm = OpenAI(openai_api_key=openai_api_key)
# llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4")


