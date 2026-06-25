import os
import google.generativeai as genai

_gemini_model = None

def get_gemini_model(model_name: str = "gemini-1.5-flash"):
    global _gemini_model
    if _gemini_model is not None:
        return _gemini_model
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        _gemini_model = False
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        model.generate_content("test")
        _gemini_model = model
        return model
    except Exception:
        _gemini_model = False
        return None

def reset_gemini_model():
    global _gemini_model
    _gemini_model = None
