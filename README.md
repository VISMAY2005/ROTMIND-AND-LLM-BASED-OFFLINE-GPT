# RotMind – LLM-Based Intelligent Assistant (Packaged Application)

## 1. Project Introduction

RotMind is a **locally runnable, LLM-based intelligent assistant** designed to demonstrate how large language models can be integrated with a **custom memory engine** and modular Python architecture.

This application has already been **packaged into a standalone executable**. Users are not required to run Python scripts or install dependencies manually. The system relies on **Ollama** for local LLM inference and communicates with a locally installed model.

The project is intended for **academic demonstration, experimentation, and learning purposes**, with emphasis on application architecture and local LLM integration.

------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 2. Project Objectives

- To demonstrate a complete LLM-based application workflow
- To integrate a local LLM runtime using Ollama
- To implement a custom memory engine for contextual persistence
- To package a Python-based AI system into a standalone executable
- To enable easy execution without requiring Python knowledge

----------------------------------------------------------------------------------------------------------------------------------------------

## 3. Technologies Used

- **Python 3**
  - Core application logic and modular architecture

- **Ollama**
  - Local LLM runtime environment
  - Handles model inference locally

- **Large Language Models**
  - Any Ollama-supported model (e.g., Llama, Mistral, Gemma)

- **PyInstaller**
  - Used to package the application into an executable file

---------------------------------------------------------------------------------------------------------------------------------------------

## 4. Application Features

- Local LLM-powered responses
- Offline model execution using Ollama
- Custom memory engine for contextual continuity
- Modular design for easy extension
- Theme-based output formatting
- Standalone executable distribution
- No cloud dependency for inference

------------------------------------------------------------------------------------------------------------------------------------------

## 5. File and Folder Structure

rotmind/
│
├── build/
│ └── PyInstaller build artifacts (auto-generated)
│
├── dist/
│ └── rotmind.exe
│ └── Standalone executable file
│
├── llm_client.py
│ └── Handles interaction with Ollama and the LLM model
│
├── main.py
│ └── Main application entry point
│ └── Coordinates LLM calls, memory handling, and execution flow
│
├── main.spec
│ └── PyInstaller specification file
│ └── Defines how the executable is built
│
├── memory_engine.py
│ └── Custom memory management module
│ └── Stores and retrieves conversational context
│
├── themes.py
│ └── Output theming and formatting logic
│
├── utils.py
│ └── Shared utility and helper functions
│
├── utils.py.txt
│ └── Reference or backup copy of utility logic
│
├── requirements.txt
│ └── Python dependencies (for development only)
│
└── README.md
└── Project documentation
------------------------------------------------------------------------------------------------------------------------------------------------

## 6. Installation and Execution Instructions

### Step 1: Install Ollama

Download and install Ollama from the official website:

- https://ollama.com

Ensure Ollama is successfully installed and running on your system.

-------------------------------------------------------------------------------------------------------------------------------------

### Step 2: Pull an LLM Model

After installing Ollama, open a terminal or command prompt and run:


You may replace `llama3` with any other supported model as required.

------------------------------------------------------------------------------------------------------------------------------------

### Step 3: Run the Application

1. Navigate to the project folder
2. Open the `dist/` directory
3. Double-click the executable file to launch the application

dist/
└── rotmind.exe
No additional setup is required.

--------------------------------------------------------------------------------------------------------------------------------------------

## 7. Usage Notes

- Ollama **must be running** before launching the executable
- The application communicates with the local Ollama instance
- Internet connection is not required after the model is downloaded
- The application runs entirely on the local machine

-----------------------------------------------------------------------------------------------------------------------------------------

## 8. Limitations

- Requires Ollama to be installed separately
- Limited to Ollama-supported models
- Uses a lot of CPU/GPU usage


------------------------------------------------------------------------------------------------------------------------------------------

## 9. Disclaimer

This project is developed **solely for educational and experimental purposes**.  
It is not intended for production deployment.  
All LLM models and runtimes are subject to their respective licenses.

-----------------------------------------------------------------------------------------------------------------------------------------


