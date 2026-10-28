import re
from typing import Dict, Any, List


class ClauseSplitter:
    def split_document(self, text: str, source_type: str = "text", pages: List[Dict] = None) -> Dict[str, Any]:
        sections = []
        source_id_counter = 1
        
        # Try to split by common legal patterns
        # Look for numbered clauses, headings
        # Split by double newlines first
        paragraphs = re.split(r'\n\n+', text)
        
        for para in paragraphs:
            para = para.strip()
            if not para or len(para) < 10:
                continue
            
            # Try to extract heading/number
            heading = None
            # Look for patterns like "1.", "Article 1", "Section 1.1", etc.
            heading_match = re.match(r'^((?:\d+\.?)+\s+|Article\s+\d+[:\.]?\s*|Section\s+[\d\.]+[:\.]?\s*|Clause\s+\d+[:\.]?\s*)(.+?)(?:\n|$)', para, re.IGNORECASE | re.DOTALL)
            if heading_match:
                heading = (heading_match.group(1) + heading_match.group(2).split('\n')[0]).strip()
            else:
                # Check if it's all caps or short line followed by content
                lines = para.split('\n')
                if len(lines) > 0 and len(lines[0]) < 100 and lines[0].isupper() and len(lines[0]) > 3:
                    heading = lines[0].strip()
            
            source_id = f"C{source_id_counter:02d}"
            source_id_counter += 1
            
            section = {
                "source_id": source_id,
                "heading": heading,
                "text": para,
                "page_number": None
            }
            
            # For PDF, try to assign page numbers (basic approximation)
            if source_type == "pdf" and pages:
                # Simple approach - assign based on content presence
                for p in pages:
                    if para[:50] in p['text']:
                        section["page_number"] = p['page_number']
                        break
            
            sections.append(section)
        
        return {
            "sections": sections,
            "total_sections": len(sections),
            "source_ids": [s["source_id"] for s in sections]
        }
