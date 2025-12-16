# RotMind – LLM-Based Intelligent Assistant

## 1. Project Introduction

RotMind is a **locally runnable, LLM-based intelligent assistant** built using Python and designed to demonstrate how large language models can be integrated with a **custom memory engine** and a modular application architecture.

Due to size limitations, the **packaged executable is not included in this repository**. Instead, the **source code is provided**, and users may run the application directly using Python or package it into an executable later if required.


----------------------------------------------------------------------------------

## 2. Project Objectives

- To design a modular LLM-based application
- To integrate a local LLM runtime using Ollama
- To implement a custom memory engine for contextual persistence
- To provide a clean and extensible Python codebase
- To allow optional packaging into a standalone executable

-----------------------------------------------------------------------------------------

## 3. Technologies Used

- **Python 3**
  - Core application logic and modular structure

- **Ollama**
  - Local LLM runtime for model inference

- **Large Language Models**
  - Any Ollama-supported model (e.g., Llama, Mistral, Gemma)

- **PyInstaller (Optional)**
  - Can be used to package the application into an executable

----------------------------------------------------------------------------------------------------

## 4. Application Features

- Local LLM-powered responses
- Offline model execution using Ollama
- Custom memory engine for maintaining context
- Modular and extensible architecture
- Theme-based output formatting
- Command-line based interaction

----------------------------------------------------------------------------------------------------------

## 5. File and Folder Structure

rotmind/
│
├── llm_client.py
│ └── Handles communication with Ollama and the LLM model
│
├── main.py
│ └── Application entry point
│ └── Manages user interaction and system flow
│
├── memory_engine.py
│ └── Custom memory management module
│ └── Stores and retrieves conversational context
│
├── themes.py
│ └── Output formatting and theme handling
│
├── utils.py
│ └── Shared helper and utility functions
│
├── utils.py.txt
│ └── Reference or backup utility file
│
├── requirements.txt
│ └── Python dependencies for running the project
│
├── main.spec
│ └── PyInstaller configuration file (optional)
│
└── README.md
└── Project documentation
---------------------------------------------------------------------------------------------------------------------------------

## 6. Installation and Setup

### Step 1: Install Python

Ensure **Python 3.9 or later** is installed on your system.

------------------------------------------------------------------------------------------------------------------------------------

### Step 2: Install Ollama

Download and install Ollama from the official website:

https://ollama.com
Verify installation by running:

ollama --version

yaml
Copy code

---

### Step 3: Pull an LLM Model

Pull any supported model using Ollama:

ollama pull llama3

yaml
Copy code

You may replace `llama3` with another model if required.

---

### Step 4: Install Python Dependencies

Navigate to the project directory and run:

pip install -r requirements.txt

yaml
Copy code
-----------------------------------------------------------------------------------------------------
## 7. Running the Application

To run RotMind directly from source code:

python main.py


Copy code

Ensure Ollama is running in the background before executing the application.

--------------------------------------------------------------------------------------------------------------------------------

## 8. Optional: Packaging the Application

If required, the application can be packaged into an executable using PyInstaller:

pyinstaller main.spec


Copy code

The packaged executable will be generated in the `dist/` directory.

-------------------------------------------------------------------------------------------------------------------

## 9. Limitations

- Requires Ollama to be installed locally
- Depends on locally available LLM models
- Command-line interface only
- No packaged executable included in the repository

----------------------------------------------------------------------------------------------------------

## 10. Disclaimer

This project is created **solely for educational and academic purposes**.  
It is not intended for commercial or production use.  
All referenced tools and models are subject to their respective licenses.

-------------------------------------------------------------------------------------------------------
