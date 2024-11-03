## Teeny Tiny Compiler
This is tiny compiler of simple pseudo-code

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the Application](#running-the-application)
5. [Using a Virtual Environment (Optional)](#using-a-virtual-environment-optional)

## Overview

This project includes a backend API server (using FastAPI) and a frontend application served locally. Once set up, you can access:
- **API Server** at `http://127.0.0.1:8000`
- **Frontend App** at `http://127.0.0.1:8888`

## Prerequisites

1. **Python Installation**  
   This project requires Python to run. If Python is not installed on your system, follow these instructions to download and install it:
   - **Windows**: [Download Python Installer](https://www.python.org/ftp/python/3.10.7/python-3.10.7-amd64.exe) and follow the setup instructions.
   - **macOS**: Visit [Python for macOS](https://www.python.org/downloads/macos/) and download the installer.
   - **Linux**: Use your package manager, e.g., `sudo apt install python3` for Ubuntu.

   > **Note**: To verify if Python is installed, open a terminal or command prompt and run:
   > ```bash
   > python --version
   > ```
   > If Python is installed, you should see a version number.

## Installation

1. **Download the Repository Files**  
   - Clone this repository using Git:
     ```bash
     git clone https://github.com/your-username/your-repo-name.git
     cd your-repo-name
     ```
   - Alternatively, download the ZIP file from GitHub and extract it.

2. **Set Up Libraries**
   - Run `setup.py` to install the required libraries:
     ```bash
     python setup.py
     ```
   - This script automatically installs all dependencies listed in `requirements.txt`.

## Running the Application

1. **Start the Application**  
   Run the main script to start both the backend API server and the frontend application:
   ```bash
   python main.py

