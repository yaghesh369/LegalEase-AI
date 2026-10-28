from typing import Dict, Any
from core.gemini_client import GeminiClient


class RiskAnalyzer:
    def __init__(self):
        self.client = GeminiClient()
    
    def analyze_risks(self, document: Dict[str, Any]) -> Dict[str, Any]:
        if not self.client.is_available():
            raise ValueError("Gemini API not configured")
        
        text = document.get('text', '')
        sections = document.get('sections', [])
        source_ids = document.get('source_ids', [])
        
        context = f"Document: {document.get('title')}\n\n"
        # Include sections with IDs
        for s in sections[:20]:
            context += f"[{s['source_id']}] {s.get('heading', '')}\n{s['text'][:300]}\n\n"
        
        system_prompt = """You are a risk analyzer for legal documents. Identify potentially unfavorable provisions.
        Only report risks actually present in the document. Do NOT label as illegal.
        Distinguish facts from interpretation. Assign severity as High, Medium, or Low."""
        
        user_prompt = f"""{context}

Analyze for risks and return JSON:
{{
  "risks": [
    {{
      "title": "risk title",
      "severity": "High|Medium|Low",
      "why_it_matters": "explanation",
      "source_ids": ["C01"],
      "page": null or number,
      "excerpt": "supporting excerpt from document"
    }}
  ]
}}

Look for: automatic renewal, non-refundable, liability exclusions, indemnification, unilateral changes, 
cancellation restrictions, data sharing, arbitration, strict deadlines/penalties.
If no risks found, return empty array. Only use source IDs from: {source_ids}"""
        
        try:
            result = self.client.generate_json(user_prompt, system_prompt)
            return {"success": True, "risks": result.get('risks', [])}
        except Exception as e:
            return {"success": False, "error": str(e)}
