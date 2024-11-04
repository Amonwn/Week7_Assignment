import streamlit as st
from openai import OpenAI
import os

st.title("Share with us your experience of the latest trip")

### Load your API Key
os.environ["OPENAI_API_KEY"] = st.secrets["OpenAIkey"]

### OpenAI stuff
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
