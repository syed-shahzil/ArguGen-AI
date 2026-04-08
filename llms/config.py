import os
from openai import OpenAI
from openai import OpenAI as OpenRouterClient

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


openai_client = OpenAI(
api_key=OPENAI_API_KEY
)


openrouter_client = OpenRouterClient(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

OLLAMA_BASE_URL = "http://localhost:11434"
ollama_url = f"{OLLAMA_BASE_URL}/api/chat"
    

# VOICE Config
favor_voice= "alloy"
opposition_voice= "verse"
judge_voice ="sage"
