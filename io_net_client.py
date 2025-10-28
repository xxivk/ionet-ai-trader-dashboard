import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class IOIntelligenceClient:
    """
    A simple client for communicating with IO.net Intelligence API.
    Supports chat completions (LLM requests).
    """

    def __init__(self, api_key: str | None = None,
                 base_url: str = "https://api.intelligence.io.solutions/api/v1"):
        self.api_key = api_key or os.getenv("IOINTELLIGENCE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing IOINTELLIGENCE_API_KEY in environment variables or .env file")

        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def chat(self,
             messages: List[Dict[str, str]],
             model: str = "deepseek-ai/DeepSeek-R1-0528",
             temperature: float = 0.7) -> str:
        """
        Send a chat completion request to IO.net model.
        """
        url = f"{self.base_url}/chat/completions"
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }

        resp = requests.post(url, headers=self.headers, json=data, timeout=600)
        resp.raise_for_status()

        result = resp.json()
        return result["choices"][0]["message"]["content"]

