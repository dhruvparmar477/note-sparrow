import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables (including API key)
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
models = genai.list_models()
for model in models:
    print(f"Model: {model.name} - Supported Methods: {model.supported_generation_methods}")
