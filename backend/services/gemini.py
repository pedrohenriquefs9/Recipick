from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
modelo = genai.GenerativeModel("gemini-1.5-flash")