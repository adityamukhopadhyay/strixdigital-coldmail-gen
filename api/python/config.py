import os
from openai import AsyncOpenAI

def create_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")
        
    return AsyncOpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        http_client=None  # Force using the default HTTP client without proxy settings
    ) 