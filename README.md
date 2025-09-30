# Vibecode Editor

A web-based tool that uses the Gemini API to transform your code based on a selected "vibe." Write or paste your code, choose a transformation, and let AI handle the rest.


---

## Features

- **AI-Powered Code Transformation:** Utilizes the Google Gemini API to refactor, translate, or analyze your code.
- **Dual Code Editor UI:** A side-by-side view using the Monaco Editor (powering VS Code) to compare the original and transformed code.
- **Multiple "Vibes":** Choose from a list of transformations, such as making code more professional, adding docstrings, or translating between languages.
- **Syntax Highlighting:** Supports a variety of popular programming languages.
- **Modern Frontend:** A stylish and responsive UI built with React and Vite.
- **FastAPI Backend:** A high-performance Python backend to handle API requests to Gemini.

---

## Technology Stack

- **Frontend:**
  - **Framework:** React (with TypeScript)
  - **Build Tool:** Vite
  - **Code Editor:** Monaco Editor (`@monaco-editor/react`)
  - **API Client:** Axios

- **Backend:**
  - **Framework:** FastAPI
  - **Language:** Python
  - **API Integration:** Google Generative AI (`google-generativeai`)
  - **Server:** Uvicorn

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js and npm:** [Download here](https://nodejs.org/)
- **Python 3.8+ and pip:** [Download here](https://www.python.org/)
- **A Google Gemini API Key:** [Get one here](https://makersuite.google.com/app/apikey)

---

## Setup and Installation

Follow these steps to get the application running locally.

### 1. Clone the Repository

First, clone this project to your local machine (or simply use the files as they are).

### 2. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    And activate it:
    - On Windows: `.\venv\Scripts\activate`
    - On macOS/Linux: `source venv/bin/activate`

3.  **Create a `.env` file** in the `backend` directory. This file will hold your secret API key. Add your Gemini API key to it:
    ```
    GEMINI_API_KEY="your_api_key_here"
    ```

4.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload
    ```
    The backend will now be running on `http://localhost:8000`.

### 3. Frontend Setup

1.  **Open a new, separate terminal**.

2.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

3.  **Install the Node.js dependencies:**
    ```bash
    npm install
    ```

4.  **Run the frontend development server:**
    ```bash
    npm run dev
    ```
    This will automatically open the Vibecode Editor in your web browser, usually at `http://localhost:5173`.

---

## How to Use

1.  Open the application in your browser.
2.  Select the programming language of your code from the dropdown.
3.  Write or paste your code into the **Input** editor on the left.
4.  Choose the desired transformation from the **Select Vibe** dropdown.
5.  Click the **Vibe Check** button.
6.  The AI-transformed code will appear in the **Output** editor on the right.
