from utils.validators import validate_pasted_text, normalize_whitespace, validate_source_references

def test_empty_text():
    ok, msg = validate_pasted_text("")
    assert not ok
    assert "No text provided" in msg

def test_short_text():
    ok, msg = validate_pasted_text("hello world")
    assert not ok
    assert "too short" in msg.lower()

def test_valid_text():
    ok, msg = validate_pasted_text("This is a valid legal document with enough content to analyze.")
    assert ok
    assert msg == ""

def test_normalize_whitespace():
    text = "Hello   world\n\n\n\nTest\t\tcase"
    norm = normalize_whitespace(text)
    assert "   " not in norm
    assert "\t" not in norm
    assert "\n\n\n" not in norm

def test_normalize_preserves_paragraphs():
    text = "Para1\n\nPara2"
    norm = normalize_whitespace(text)
    assert "\n\n" in norm

def test_source_validation():
    valid, invalid = validate_source_references(["C01", "C99"], {"C01", "C02", "C03"})
    assert "C01" in valid
    assert len(invalid) == 1
    assert invalid[0]["source_id"] == "C99"
