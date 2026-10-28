import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv(override=True)

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


class GeminiClient:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.client = None
        if self.api_key and genai:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                self.client = None
                raise e
    
    def is_available(self) -> bool:
        return self.client is not None and self.api_key is not None
    
    def generate_content(self, prompt: str, system_instruction: Optional[str] = None, 
                         temperature: float = 0.1, max_tokens: int = 8192) -> str:
        if not self.is_available():
            raise ValueError("Gemini API client not available. Please check your API key.")
        
        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            if system_instruction:
                config.system_instruction = system_instruction
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def generate_json(self, prompt: str, system_instruction: Optional[str] = None) -> dict:
        import json
        text = self.generate_content(prompt, system_instruction, temperature=0.1)
        text = text.strip()
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            if end > start:
                text = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            if end > start:
                text = text[start:end].strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from model: {str(e)}\nResponse: {text[:200]}")
