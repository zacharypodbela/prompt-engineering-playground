# Quickstart

## Setup Dependancies

### Ollama

1. [Download Ollama](https://ollama.ai/download/Ollama-darwin.zip)
2. Double click the zip file you downloaded and your computer should automatically unzip it into the Ollama application.
3. Double click on "Ollama" application and follow instructions on screen.
4. In Terminal, type `ollama pull llama2` and press Enter.

### Homebrew and Pipenv

From Terminal, run the folowing commands one at a time (type them in or copy and paste them in and then press Enter):

1. `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. `brew install pipenv`

### Open AI

1. [Sign up for Open AI](https://platform.openai.com/signup)
2. In the settings area of your developer account, generate a new API key and save it on your computer to use later (i.e. in Notes or something similar)

## Download and Setup this Project

1. [Download the project](https://github.com/ollama/ollama/archive/refs/heads/main.zip)
2. Double click the zip file you downloaded and your computer should automatically unzip it into a folder
3. In Terminal, type `cd ` and then drag the folder into the terminal window. The text in Terminal should now look something like `cd /Users/...`. Press Enter.
4. Type `echo "OPENAI_API_KEY=` followed by your Open AI key then type `" >> .env` and press Enter.
5. Type `pipenv install` and press Enter.

## Run the Project

Follow these steps whenever you want to run the project.

1. In Terminal, type `cd ` and then drag the folder into the terminal window. The text in Terminal should now look something like `cd /Users/...`. Press Enter.
2. Type `pipenv shell` and press Enter.
3. Type `streamlit run app.py` and press Enter.
4. A chrome window should open up where you can interact with the AI!
