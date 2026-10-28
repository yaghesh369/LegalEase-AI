from utils.validators import normalize_whitespace


class TextProcessor:
    def process_text(self, text: str, title: str = None) -> dict:
        normalized = normalize_whitespace(text)
        return {
            "success": True,
            "text": normalized,
            "title": title or "Pasted Legal Text",
            "source_type": "text"
        }
