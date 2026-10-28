from typing import Dict, Any
from core.gemini_client import GeminiClient


class CrossReferenceAnalyzer:
    def __init__(self):
        self.client = GeminiClient()
    
    def find_cross_references(self, document: Dict[str, Any]) -> Dict[str, Any]:
        if not self.client.is_available():
            raise ValueError("Gemini API not configured")
        
        sections = document.get('sections', [])
        source_ids = document.get('source_ids', [])
        
        context = ""
        for s in sections[:30]:
            context += f"[{s['source_id']}] {s.get('heading', 'No heading')}\n{s['text'][:400]}\n\n"
        
        system_prompt = """You find relationships between clauses that affect understanding.
        ONLY report connections supported by the document. Do not invent references.
        Be specific about why clauses are connected."""
        
        user_prompt = f"""{context}

Find cross-references and return JSON:
{{
  "cross_references": [
    {{
      "source_ids": ["C01", "C02"],
      "headings": ["heading1", "heading2"],
      "connection_reason": "why connected",
      "practical_implication": "implication for reader",
      "evidence_snippets": ["snippet from doc"]
    }}
  ]
}}

Only use source IDs from: {source_ids}. If none, return empty array."""
        
        try:
            result = self.client.generate_json(user_prompt, system_prompt)
            return {"success": True, "cross_references": result.get('cross_references', [])}
        except Exception as e:
            return {"success": False, "error": str(e)}
