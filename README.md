# Prompt Engineering Playground

An intuitive web UI enabling non-technical users to test different prompts with a variety of AI models.

## Setup

**Video Walkthrough (5 mins) of Steps Below**

https://www.loom.com/share/b6760bcabf9547d9bc2934c3fcf9e1f0?sid=f9d8b0e2-d622-4063-807d-d8942ea96ea1

### Ollama

1. [Download Ollama](https://ollama.ai/download/Ollama-darwin.zip)
2. Double click the zip file you downloaded and your computer should automatically unzip it into the Ollama application.
3. Double click on "Ollama" application and follow instructions on screen.
4. In Terminal, type `ollama pull llama2` and press Enter.

### Homebrew and Pipenv

From Terminal, run the folowing commands one at a time (type them in or copy and paste them in and then press Enter):

1. `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/ralphjsmit/.zprofile` (Homebrew will tell you to run this in the "Next Steps")
3. `eval "$(/opt/homebrew/bin/brew shellenv)"` (Homebrew will tell you to run this in the "Next Steps")
4. `brew install pipenv`

### Open AI

1. [Sign up for Open AI](https://platform.openai.com/signup)
2. In [User settings > API Keys](https://platform.openai.com/api-keys), click "Create new secret key", give it a name, and then save it to use later. (Note: Once you close this page, you will not be able to see the key again and will need to generate a new on if you lose it.)

### This Project

1. [Download the project](https://github.com/zacharypodbela/prompt-engineering-playground/archive/refs/heads/main.zip)
2. Double click the zip file you downloaded and your computer should automatically unzip it into a folder
3. In Terminal, type `cd ` and then drag the folder into the terminal window. The text in Terminal should now look something like `cd /Users/...`. Press Enter.
4. Type `echo "OPENAI_API_KEY=` followed by your Open AI key then type `" >> .env` and press Enter.
5. Type `pipenv install` and press Enter.

## Running the Program

Follow these steps whenever you want to run the project.

1. In Terminal, type `cd ` and then drag the folder into the terminal window. The text in Terminal should now look something like `cd /Users/...`. Press Enter.
2. Type `pipenv shell` and press Enter.
3. Type `streamlit run app.py` and press Enter.
4. A chrome window should open up where you can interact with the AI!

## Roadmap

Future improvements to be added to the project:

- [ ] Enable different Ollama and Open AI models to be choosen from a dropdown
