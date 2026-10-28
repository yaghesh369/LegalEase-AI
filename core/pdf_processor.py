from typing import Dict, Any, List


class PDFProcessor:
    def extract_text(self, pdf_file) -> Dict[str, Any]:
        try:
            # Load the native PDF dependency only when a PDF is actually uploaded.
            # This keeps text mode available if the local PyMuPDF binary is
            # incompatible with the installed Python runtime.
            try:
                import fitz  # PyMuPDF
            except ImportError as exc:
                return {
                    "success": False,
                    "error": (
                        "PDF support is unavailable because PyMuPDF could not be "
                        f"loaded: {exc}. Use a supported Python version and reinstall "
                        "the dependencies."
                    )
                }

            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            pages_data = []
            full_text = []
            
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text()
                if text.strip():
                    pages_data.append({
                        "page_number": page_num,
                        "text": text
                    })
                    full_text.append(text)
            
            doc.close()
            
            if not full_text or all(not p.strip() for p in full_text):
                return {
                    "success": False,
                    "error": "No extractable text found. This may be a scanned PDF which requires OCR (not included in this version)."
                }
            
            combined_text = "\n\n".join(full_text)
            return {
                "success": True,
                "text": combined_text,
                "pages": pages_data,
                "page_count": len(pages_data),
                "filename": getattr(pdf_file, 'name', 'uploaded.pdf')
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to process PDF: {str(e)}"
            }
