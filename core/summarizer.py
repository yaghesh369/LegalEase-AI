from typing import Dict, Any
from core.gemini_client import GeminiClient


class Summarizer:
    def __init__(self):
        self.client = GeminiClient()
    
    def generate_summary(self, document: Dict[str, Any]) -> Dict[str, Any]:
        if not self.client.is_available():
            raise ValueError("Gemini API not configured. Please set GEMINI_API_KEY in .env")
        
        text = document.get('text', '')
        sections = document.get('sections', [])
        
        # Prepare context
        context = f"Document Title: {document.get('title', 'Untitled')}\n\n"
        context += text[:15000]  # Limit context
        
        system_prompt = """You are a legal document simplifier. Your job is to explain legal documents in plain English for non-lawyers.
        Do NOT fabricate information. Only state what is actually in the document.
        Clearly indicate if information is not mentioned.
        Be accurate and educational."""
        
        user_prompt = f"""{context}

Provide a structured summary in JSON format with the following keys:
{{
  "what_is_it": "Brief description of what this document is",
  "main_purpose": "Main purpose",
  "key_terms_conditions": ["list of key terms"],
  "user_rights": ["user rights mentioned"],
  "responsibilities_obligations": ["obligations of user/parties"],
  "fees_charges": ["fees or state if none mentioned"],
  "cancellation_termination": ["cancellation terms or state if none"],
  "renewal_conditions": ["renewal terms or state if none"],
  "data_collection_privacy": ["data/privacy terms or state if not mentioned"],
  "dispute_resolution_governing_law": ["dispute resolution or state if not mentioned"]
}}

Only include information actually present in the document."""
        
        try:
            result = self.client.generate_json(user_prompt, system_prompt)
            return {"success": True, "summary": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
