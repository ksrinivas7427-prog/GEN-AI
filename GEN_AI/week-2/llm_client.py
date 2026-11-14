from abc import ABC, abstractmethod

try:
    from google import genai
except ImportError:  # pragma: no cover - only used when Gemini is unavailable
    genai = None

import requests


# Common interface
class LLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt):
        pass


# Gemini cloud provider
class GeminiProvider(LLMProvider):

    def __init__(self, api_key):
        if genai is None:
            raise ModuleNotFoundError(
                "The 'google-genai' package is required for the Gemini provider. "
                "Install it with: pip install google-genai"
            )

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return response.text


# Ollama local provider
class OllamaProvider(LLMProvider):

    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        return response.json()["response"]


# Common client
class LLMClient:

    def __init__(self, provider):
        self.provider = provider

    def generate(self, prompt):
        return self.provider.generate(prompt)
