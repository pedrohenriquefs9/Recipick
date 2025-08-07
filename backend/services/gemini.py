import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi definida.")

genai.configure(api_key=api_key)

generation_config = genai.types.GenerationConfig(
    response_mime_type="application/json"
)

modelo = genai.GenerativeModel("gemini-1.5-pro")