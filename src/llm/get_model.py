import os
import google.generativeai as genai
from tools.tools import tools

_model = None


def get_model():
    global _model
    if _model is not None:
        return _model

    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("MODEL_NAME")

    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada nas variáveis de ambiente.")

    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }

    _model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        tools=tools,
    )

    return _model
