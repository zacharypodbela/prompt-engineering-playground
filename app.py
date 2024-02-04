from dotenv import load_dotenv

import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

## OpenAI Initialization

# Set the OpenAI model here with model_name=
# "text-davinci-003" (the default) is the most powerful but costs $0.02/1000 (very expensive)
# In order of decreasing power and cost the other options are: 
# "text-curie-001" (1/10 the cost of davinci)
# "text-babbage-001" (1/40 the cost of davinci)
# "text-ada-001" (1/50 the cost of davinci)
# You can also use non-OpenAI models by instantiating a different LLM class here.
# See: https://python.langchain.com/en/latest/modules/models/llms/integrations.html
llm = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages([
    ("system", "{system}"),
    ("user", "{prompt}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

@st.cache_data
def query_openai(system, prompt):
    return chain.invoke({ "system": system, "prompt": prompt })

system = st.text_input('Enter the system instructions here:')
prompt = st.text_input('Enter your user prompt here:')
if system and prompt:
    result = query_openai(system, prompt)
    st.write(result)