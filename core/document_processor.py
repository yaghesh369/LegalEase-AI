from typing import Dict, Any
from core.pdf_processor import PDFProcessor
from core.text_processor import TextProcessor
from core.clause_splitter import ClauseSplitter


class DocumentProcessor:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.text_processor = TextProcessor()
        self.clause_splitter = ClauseSplitter()
    
    def process_pdf(self, pdf_file) -> Dict[str, Any]:
        result = self.pdf_processor.extract_text(pdf_file)
        if not result.get('success'):
            return result
        
        split_result = self.clause_splitter.split_document(
            result['text'], 
            source_type='pdf',
            pages=result.get('pages', [])
        )
        
        return {
            "success": True,
            "title": result.get('filename', 'Uploaded PDF'),
            "source_type": "pdf",
            "text": result['text'],
            "pages": result.get('pages', []),
            "sections": split_result['sections'],
            "source_ids": split_result['source_ids']
        }
    
    def process_text(self, text: str, title: str = None) -> Dict[str, Any]:
        result = self.text_processor.process_text(text, title)
        if not result.get('success'):
            return result
        
        split_result = self.clause_splitter.split_document(
            result['text'],
            source_type='text'
        )
        
        return {
            "success": True,
            "title": result.get('title', 'Pasted Text'),
            "source_type": "text",
            "text": result['text'],
            "pages": [],
            "sections": split_result['sections'],
            "source_ids": split_result['source_ids']
        }
