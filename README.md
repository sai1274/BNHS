# BNHS

## Introduction
 Bombay Natural History Society (BNHS) is a project designed to increase the user engament for [BNHS](https://bnhs.org/). This document provides steps for setting up and running the project.

## Prerequisites
Before running the project, ensure you have the following installed:
- Python (>= 3.11)
- Git

## Installation
Follow these steps to set up the project on your local machine:

1. **Clone the repository**
   ```sh
   git clone https://github.com/sai1274/BNHS.git
   cd BNHS
   ```

2. **Create and activate a virtual environment** (optional but recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Download and Set Up Ollama on macOS**
   
   To install Ollama, run the following command:
   ```sh
   curl -fsSL https://ollama.ai/install.sh | sh
   ```
   
   After installation, restart your terminal or run:
   ```sh
   source ~/.zshrc  # If using zsh
   source ~/.bashrc  # If using bash
   ```

5. **Verify Ollama Installation**
   To confirm Ollama is installed correctly, run:
   ```sh
   ollama --version
   ```
   
6. **Download and Install the Llama2 Model**
   ```sh
   ollama pull llama2:latest
   ```

7. **Run Ollama Server Locally**
   ```sh
   ollama serve
   ```
   This will host the model locally for inference.

## Usage
To run the project, execute:
```sh
uvicorn fastapi_server:app --host 0.0.0.0 --port 11434
```

## Integrating UI with the Backend
If you have a UI folder and need to integrate it with the backend, follow these steps:

1. **Navigate to the UI directory**
   ```sh
   cd UI
   ```

2. **Open the UI in a browser**
   - Simply open the `main_ui.html` file in any browser.
   - Ensure the backend (`ollama serve`) is running to support AI-based functionality.

3. **Configure API endpoints if needed**
   - If the frontend needs to communicate with the backend, update any JavaScript files to point to the backend API (e.g., `http://localhost:5000`).

4. **Update the address in `script.js` to the IP address of the system where the backend is running.**
   
   To find the IP address of the system, run the following command in the terminal:
   ```sh
   ifconfig | grep inet
   ```
   Then, update the address in `script.js` accordingly.

## Scheduling Monthly Newsletter Summary with Cron
To automatically send a summary of the newsletter released for the month, add the following line to your crontab:
```sh
0 10 * * 1 venv/pythonpath mail_and_news_letter.py
```
This will run the script every Monday at 10:00 AM.

To add this job to crontab, run:
```sh
crontab -e
```
Then paste the above line and save the file.