from dotenv import load_dotenv
from string import Formatter

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

def init_chain(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system}"),
        ("user", "{prompt}")
    ])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain

@st.cache_data
def query_openai(system, prompt):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo-0125')
    chain = init_chain(llm)
    return chain.invoke({ "system": system, "prompt": prompt })

@st.cache_data
def query_ollama(system, prompt):
    llm = Ollama(model="llama2")
    chain = init_chain(llm)
    return chain.invoke({ "system": system, "prompt": prompt })

st.header("Model Input")
system, prompt = None, None # system and prompt will be the outputs of this section
prompt_buidler_modes = ["Plain Text Prompt Entry", "Templates and Variable Prompt Builder"]
prompt_builder_mode = st.radio("Choose whether to enter exact system and user prompts or build prompts using templates and data:", prompt_buidler_modes)
prompt_builder_i = prompt_buidler_modes.index(prompt_builder_mode)
if prompt_builder_i == 0:
    # Prompt Entry Fields
    system = st.text_input('Enter the system instructions here:', value="Always speak in a friendly way.")
    prompt = st.text_input('Enter your user prompt here:', value="Can you tell me about science?")
elif prompt_builder_i == 1:
    # Template Entry
    _system = st.text_input('Enter the system instructions *template* here:', value="Always speak in a {tone} way.")
    _prompt = st.text_input('Enter your user prompt here:', value="Can you tell me about {topic}?")
    template_keys = [i[1] for i in Formatter().parse(_system+" "+_prompt) if i[1] is not None]

    # Data Editor
    st.write("Add your data to be inserted in the templates above here:")
    edited_data = st.data_editor({
        "tone": "friendly",
        "topic": "science"
    }, use_container_width=True, num_rows="dynamic")
    missing_keys = [key for key in template_keys if key not in edited_data]

    # Prompt Preview
    with st.container(border=True):
        st.subheader("Compiled Prompt")
        if missing_keys:
            st.markdown(f"⛔️ Set the following missing variables to generate prompts: `{'`, `'.join(missing_keys)}`")
        else:
            system = _system.format(**edited_data)
            prompt = _prompt.format(**edited_data)
            st.write(f"System instructions that will be passed to model:")
            st.markdown(f"```{system}```")
            st.write(f"User prompt that will be passed to model:")
            st.markdown(f"```{prompt}```")

st.header("Model Settings")
llm_choice = st.radio("Choose the language model", ("Ollama (Free)", "OpenAI (Paid)"))

st.header("Model Response")
if system and prompt and llm_choice:
    result = query_ollama(system, prompt) if llm_choice == "Ollama (Free)" else query_openai(system, prompt)
    st.write(result)
else:
    if not system or not prompt:
        st.write("⛔️ Finish entering or building your input prompts to generate an output.")
    if not llm_choice:
        st.write("⛔️ Finish selecting configurations for the model in the Model Settings section to generate an output.")