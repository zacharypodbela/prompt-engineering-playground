from dotenv import load_dotenv
from string import Formatter

import streamlit as st
from pydash import partition

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

## Model Functions

def init_chain(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system}"),
        ("user", "{prompt}")
    ])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain

@st.cache_data
def query_llm(system, prompt, llm_choice):
    if llm_choice == "OpenAI (Paid)":
        llm = ChatOpenAI(model_name='gpt-3.5-turbo-0125')
    else:
        llm = Ollama(model="llama2")

    chain = init_chain(llm)
    return chain.invoke({ "system": system, "prompt": prompt })

## State Management

if 'number_prompts' not in st.session_state:
    st.session_state.number_prompts = 1
    
def increase_prompt_count():
    st.session_state.number_prompts = st.session_state.number_prompts + 1

def decrease_prompt_count():
    st.session_state.number_prompts = st.session_state.number_prompts - 1

if 'prompt_responses' not in st.session_state:
    st.session_state.prompt_responses = {}

def save_prompt_response(prompt_index, response):
    st.session_state.prompt_responses[prompt_index] = response

def return_responses_of_previous_prompts_as_template_data(prompt_index):
    return { f"prompt_{i}": st.session_state.prompt_responses[i] for i in range(1, prompt_index) }

if 'already_ran_inputs' not in st.session_state:
    st.session_state.already_ran_inputs = set()

def mark_inputs_have_run(system, prompt, llm_choice):
    st.session_state.already_ran_inputs.add((system, prompt, llm_choice))

def inputs_have_run_before(system, prompt, llm_choice):
    return (system, prompt, llm_choice) in st.session_state.already_ran_inputs

## Streamlit UI

def validate_and_render_instructions(_input, input_label, all_data):
    st.write(f"{input_label.capitalize()} instructions that will be passed to model:")
    if _input:
        template_keys = [i[1] for i in Formatter().parse(_input) if i[1] is not None]
        missing_keys = [key for key in template_keys if key not in all_data]
        if missing_keys:
            [missing_prompt_keys, missing_normal_keys] = partition(missing_keys, lambda k: k.startswith("prompt_"))
            if missing_normal_keys:
                st.markdown(f"⛔️ Set the following missing variables to generate prompts: `{'`, `'.join(missing_normal_keys)}`")
            if missing_prompt_keys:
                st.markdown(f"⛔️ Ensure all previous prompts have run to generate values for: `{'`, `'.join(missing_prompt_keys)}`")
        else:
            input = _input.format(**all_data)
            st.markdown(f"```\n{input}\n```")
            return input
    else:
        st.write(f"⛔️ Enter a {input_label} prompt template.")

def render_prompt(index):
    multiple_prompt_mode = st.session_state.number_prompts > 1
    is_first_prompt = index == 1
    is_last_prompt = index == st.session_state.number_prompts

    if st.session_state.number_prompts > 1:
        st.title(f"Prompt {index}")
        if is_last_prompt:
            st.button("Delete this prompt", on_click=decrease_prompt_count)
    st.header("Model Input")
    system, prompt = None, None # system and prompt will be the outputs of this section
    prompt_buidler_modes = ["Plain Text Prompt Entry", "Templates and Variable Prompt Builder"]
    prompt_builder_mode = st.radio("Choose whether to enter exact system and user prompts or build prompts using templates and data:", prompt_buidler_modes, index=1 if multiple_prompt_mode and not is_first_prompt else 0, key=f"Prompt Builder Mode {index}")
    prompt_builder_i = prompt_buidler_modes.index(prompt_builder_mode)
    _system = st.text_area(f"Enter the system instructions here:", key=f"System {index}")
    _prompt = st.text_area(f"Enter your user instructions here:", key=f"Prompt {index}")
    if prompt_builder_i == 0:
        system = _system
        prompt = _prompt
    elif prompt_builder_i == 1:
        st.write("Add your data to be inserted in the templates:")
        data_frame_element_config = {
            "use_container_width": True, 
            "column_order": ["_index", "value"],
            "column_config": { "_index": "Variable Name", "value": "Value" },
        }
        edited_data = st.data_editor(
            {
                "tone": "friendly"
            },
            key=f"Data Editor {index}",
            num_rows="dynamic",
            **data_frame_element_config
        )
        data_from_previous_prompts = return_responses_of_previous_prompts_as_template_data(index)
        if data_from_previous_prompts:
            st.write("Plus you can leverage the output of previous prompts as variables in the templates:")
            st.dataframe(return_responses_of_previous_prompts_as_template_data(index), **data_frame_element_config)

        all_data = {**data_from_previous_prompts, **edited_data}
        all_data = {k: v for k, v in all_data.items() if v is not None} # Remove keys with value=None

        # Prompt Preview
        with st.container(border=True):
            st.subheader("Compiled Prompt")
            system = validate_and_render_instructions(_system, "system", all_data)
            prompt = validate_and_render_instructions(_prompt, "user", all_data)                  

    st.header("Model Settings")
    llm_choice = st.radio("Choose the language model", ("Ollama (Free)", "OpenAI (Paid)"), key=f"Model Choice {index}")
    run_on_change = st.checkbox("Automatically re-run the model on change of input?", value=llm_choice == "Ollama (Free)", key=f"Run on Change {index}")

    st.header("Model Response")
    should_run = True if run_on_change else st.button("Run Model", key=f"Run Model {index}")
    result = None
    if system and prompt and llm_choice and (should_run or inputs_have_run_before(system, prompt, llm_choice)):
        mark_inputs_have_run(system, prompt, llm_choice)
        result = query_llm(system, prompt, llm_choice)
        st.write(result)
        if is_last_prompt:
            st.button("Chain the output of this prompt to another prompt", on_click=increase_prompt_count)
        else:
            with st.container(border=True):
                st.caption(f"Use the output of this prompt in subsequent prompts by referencing {{prompt_{index}}} in the system or user prompt templates.")
    elif not system or not prompt:
        st.write("⛔️ Finish entering or building your input prompts to generate an output.")
    elif not llm_choice:
        st.write("⛔️ Finish selecting configurations for the model in the Model Settings section to generate an output.")
    save_prompt_response(index, result)

for i in range(st.session_state.number_prompts):
    render_prompt(i+1)