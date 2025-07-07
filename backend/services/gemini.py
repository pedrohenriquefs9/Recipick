import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Valida se a chave da API foi fornecida
if not api_key:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi definida.")

# Configura a biblioteca do Google AI com a chave
genai.configure(api_key=api_key)

# Define uma configuração global para forçar a IA a responder em formato JSON
generation_config = genai.types.GenerationConfig(
    response_mime_type="application/json"
)

modelo = genai.GenerativeModel("gemini-1.5-flash")
