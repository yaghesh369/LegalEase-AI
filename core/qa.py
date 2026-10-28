from typing import Dict, Any
from core.gemini_client import GeminiClient


class DocumentQA:
    def __init__(self):
        self.client = GeminiClient()
    
    def answer_question(self, document: Dict[str, Any], question: str) -> Dict[str, Any]:
        if not self.client.is_available():
            raise ValueError("Gemini API not configured")
        
        if not question or not question.strip():
            return {"success": False, "error": "Please provide a question."}
        
        sections = document.get('sections', [])
        source_ids = document.get('source_ids', [])
        
        context = f"Document: {document.get('title')}\n\n"
        for s in sections:
            context += f"[{s['source_id']}] Page: {s.get('page_number') or 'N/A'} | {s.get('heading', '')}\n{s['text']}\n\n---\n\n"
        
        system_prompt = """You answer questions about legal documents using ONLY the provided document.
        If the answer is not in the document, you MUST say "The document does not provide enough information to answer this question."
        Always cite source IDs. Never invent information."""
        
        user_prompt = f"""{context}

Question: {question}

Answer in JSON format:
{{
  "answer": "your answer",
  "source_ids": ["C01"],
  "pages": [1],
  "supporting_excerpts": ["relevant excerpt"],
  "answer_found": true/false
}}

Only use source IDs from: {source_ids}"""
        
        try:
            result = self.client.generate_json(user_prompt, system_prompt)
            return {"success": True, "qa_result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
