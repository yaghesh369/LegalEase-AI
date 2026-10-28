import re
from typing import List, Tuple


class ValidationError(Exception):
    pass


def validate_pasted_text(text: str) -> Tuple[bool, str]:
    if not text or not text.strip():
        return False, "No text provided. Please paste legal text to analyze."
    stripped = text.strip()
    if len(stripped) < 20:
        return False, "Text is too short to analyze meaningfully. Please provide more content."
    return True, ""


def normalize_whitespace(text: str) -> str:
    if not text:
        return ""
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse spaces/tabs on each line but preserve paragraph boundaries
    lines = []
    for line in text.split("\n"):
        # Preserve empty lines as paragraph breaks
        if line.strip() == "":
            lines.append("")
        else:
            # Normalize internal whitespace
            normalized = re.sub(r"[ \t]+", " ", line.strip())
            lines.append(normalized)
    # Join with newlines but collapse multiple blank lines
    result = "\n".join(lines)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def validate_source_references(source_ids: List[str], available_ids: set) -> Tuple[List[str], List[dict]]:
    valid = []
    invalid = []
    for sid in source_ids:
        if sid in available_ids:
            valid.append(sid)
        else:
            invalid.append({"source_id": sid, "issue": "not_found_in_document"})
    return valid, invalid
