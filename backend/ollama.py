from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import set_key, get_key
import os

router = APIRouter()

class OllamaKeyRequest(BaseModel):
    api_key: str

@router.post("/api/set-ollama-key")
def set_ollama_key(request: OllamaKeyRequest):
    """
    Receives an Ollama API key and saves it to the .env file.
    """
    try:
        # Path to the .env file
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

        # Create the .env file if it doesn't exist
        if not os.path.exists(dotenv_path):
            with open(dotenv_path, 'w') as f:
                pass
        
        set_key(dotenv_path, "OLLAMA_API_KEY", request.api_key)
        return {"message": "Ollama API key set successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to set Ollama API key: {str(e)}"
        )

@router.get("/api/get-ollama-key")
def get_ollama_key():
    """
    Checks if the Ollama API key is set in the .env file.
    """
    try:
        # Path to the .env file
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

        api_key = get_key(dotenv_path, "OLLAMA_API_KEY")
        
        if api_key:
            return {"api_key_set": True}
        else:
            return {"api_key_set": False}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check Ollama API key: {str(e)}"
        )
