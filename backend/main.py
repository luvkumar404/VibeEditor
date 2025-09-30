import os
import re
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from ollama import router as ollama_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# --- CORS Configuration ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ollama_router)

# --- Pydantic Models ---
class VibeRequest(BaseModel):
    code: str
    vibe: str
    language: str

# --- Utility: remove comments (heuristic) ---
def strip_comments(code: str, language: str) -> str:
    """
    Heuristic comment stripper for common languages.
    Note: not a full parser — but covers common single-line and block comments.
    """
    if not code:
        return code

    lang = (language or "").lower()
    original = code

    try:
        # Python-specific: remove triple-quoted strings (docstrings) and '#' comments
        if "python" in lang or lang in ("py", "python3", "python2"):
            # Remove triple-quoted blocks ('''...''' or """...""")
            code = re.sub(r'("""|\'\'\')(.*?)(\1)', '', code, flags=re.S)
            # Remove single-line comments that start with #
            code = re.sub(r'(?m)#.*$', '', code)
            # Collapse multiple blank lines
            code = re.sub(r'\n\s*\n+', '\n', code)
            return code.strip()

        # For C / C++ / Java / JavaScript / C# / TypeScript and similar:
        # Remove /* ... */ and // comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)        # block comments
        code = re.sub(r'(?m)//.*$', '', code)                    # single-line //
        # Also remove HTML-style comments if present
        code = re.sub(r'<!--.*?-->', '', code, flags=re.S)
        # As a fallback, also strip python-style '#'
        code = re.sub(r'(?m)#.*$', '', code)
        code = re.sub(r'\n\s*\n+', '\n', code)
        return code.strip()
    except Exception:
        # If anything goes wrong, return the original code
        return original.strip()

# --- Helper: robust text extraction from generative response ---
def extract_text_from_response(response) -> str:
    """
    Attempts several ways to pull textual content from the SDK response.
    This is defensive because different SDK versions / shapes may vary.
    """
    # 1) direct .text
    if hasattr(response, "text") and response.text:
        return response.text.strip()

    # 2) candidates -> content -> parts -> text or string
    try:
        candidates = getattr(response, "candidates", None)
        if candidates and len(candidates) > 0:
            candidate = candidates[0]
            content = getattr(candidate, "content", None)
            if content is not None:
                parts = getattr(content, "parts", None)
                if parts and len(parts) > 0:
                    part = parts[0]
                    # part might be an object with .text or a plain string
                    if hasattr(part, "text") and part.text:
                        return part.text.strip()
                    if isinstance(part, str):
                        return part.strip()
            # candidate might be a dict-like
            if isinstance(candidate, dict):
                cont = candidate.get("content")
                if isinstance(cont, dict):
                    parts = cont.get("parts")
                    if parts and len(parts) > 0:
                        first = parts[0]
                        if isinstance(first, dict):
                            return first.get("text", "").strip() or str(first).strip()
                        return str(first).strip()
    except Exception:
        pass

    # 3) try stringifying the response as a last resort
    try:
        return str(response).strip()
    except Exception:
        return ""

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Vibecode Editor Backend (Gemini Edition) is running!"}

@app.post("/api/vibe-check-ollama")
def vibe_check_ollama(request: VibeRequest):
    """
    Receives code and a "vibe," strips comments from the original code (heuristic),
    sends the cleaned code to Ollama, and returns the transformed code.
    """
    ollama_api_key = os.getenv("OLLAMA_API_KEY")
    if not ollama_api_key:
        raise HTTPException(
            status_code=500,
            detail="OLLAMA_API_KEY not found. Please set it in your .env file."
        )

    # Preprocess: remove comments from the submitted code
    cleaned_code = strip_comments(request.code, request.language)

    # If cleaning removed everything, fall back to original to avoid empty prompt
    if not cleaned_code.strip():
        cleaned_code = request.code.strip()

    try:
        # --- Prompt Engineering ---
        prompt = f"""You are an expert code assistant. Your task is to transform the following {request.language} code snippet based on the requested "vibe".

Vibe: "{request.vibe}"

Instructions:
- Only return the raw, transformed code.
- Do not add any explanations, comments, or markdown formatting (like ```) around the code.
- Ensure the output is valid {request.language} code.

Original Code (comments removed):
{cleaned_code}
"""

        # Send request to Ollama API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False
            },
            headers={
                "Authorization": f"Bearer {ollama_api_key}"
            }
        )
        response.raise_for_status()  # Raise an exception for bad status codes

        # Extract the transformed code from the response
        transformed_code = response.json().get("response", "")

        return {"transformed_code": transformed_code.strip()}

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to Ollama API: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {e}"
        )
