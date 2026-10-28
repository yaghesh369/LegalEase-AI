from core.text_processor import TextProcessor
from core.clause_splitter import ClauseSplitter

def test_text_processor():
    tp = TextProcessor()
    result = tp.process_text("  Hello   world  \n\n  Test  ", "My Doc")
    assert result["success"]
    assert result["title"] == "My Doc"
    assert result["source_type"] == "text"

def test_clause_splitter():
    cs = ClauseSplitter()
    text = "1. First clause\n\nThis is the content.\n\n2. Second clause\n\nMore content here."
    result = cs.split_document(text, source_type="text")
    assert result["total_sections"] >= 1
    assert len(result["source_ids"]) == result["total_sections"]
    assert result["source_ids"][0].startswith("C")

def test_stable_source_ids():
    cs = ClauseSplitter()
    text = "Clause one\n\nClause two\n\nClause three"
    result = cs.split_document(text, source_type="text")
    assert result["source_ids"] == ["C01", "C02", "C03"]
