import json
from datetime import datetime
from typing import Dict, Any


def export_analysis_to_markdown(analysis: Dict[str, Any], doc_info: Dict[str, Any]) -> str:
    lines = []
    lines.append(f"# LegalEase AI - Analysis Report")
    lines.append(f"")
    lines.append(f"**Document Title:** {doc_info.get('title', 'Untitled')}")
    lines.append(f"**Source Type:** {doc_info.get('source_type', 'unknown')}")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    
    # Overview/Summary
    lines.append(f"## Overview & Summary")
    summary = analysis.get('summary', {})
    if isinstance(summary, dict):
        for key, value in summary.items():
            if value:
                key_title = key.replace('_', ' ').title()
                lines.append(f"### {key_title}")
                if isinstance(value, list):
                    for item in value:
                        lines.append(f"- {item}")
                else:
                    lines.append(f"{value}")
                lines.append(f"")
    else:
        lines.append(f"{summary}")
        lines.append(f"")
    
    # Key Clauses
    lines.append(f"## Key Clauses")
    clauses = analysis.get('clauses', [])
    if clauses:
        for clause in clauses:
            lines.append(f"### {clause.get('source_id', 'N/A')} - {clause.get('heading', 'Clause')}")
            if clause.get('page'):
                lines.append(f"**Page:** {clause.get('page')}")
            lines.append(f"")
            if clause.get('original_text_excerpt'):
                lines.append(f"**Original Text:**")
                lines.append(f"```")
                lines.append(f"{clause.get('original_text_excerpt')}")
                lines.append(f"```")
                lines.append(f"")
            if clause.get('explanation'):
                lines.append(f"**Plain-English Explanation:**")
                lines.append(f"{clause.get('explanation')}")
                lines.append(f"")
            lines.append(f"---")
            lines.append(f"")
    else:
        lines.append(f"*No clauses extracted.*")
        lines.append(f"")
    
    # Risks
    lines.append(f"## Potential Risks & Important Conditions")
    risks = analysis.get('risks', [])
    if risks:
        for risk in risks:
            severity = risk.get('severity', 'Unknown')
            lines.append(f"### [{severity}] {risk.get('title', 'Risk')}")
            if risk.get('source_ids'):
                lines.append(f"**Source References:** {', '.join(risk.get('source_ids', []))}")
            if risk.get('page'):
                lines.append(f"**Page:** {risk.get('page')}")
            lines.append(f"")
            if risk.get('why_it_matters'):
                lines.append(f"**Why it matters:** {risk.get('why_it_matters')}")
                lines.append(f"")
            if risk.get('excerpt'):
                lines.append(f"**Supporting excerpt:**")
                lines.append(f"```")
                lines.append(f"{risk.get('excerpt')}")
                lines.append(f"```")
                lines.append(f"")
            lines.append(f"---")
            lines.append(f"")
    else:
        lines.append(f"*No specific risks identified.*")
        lines.append(f"")
    
    # Cross References
    lines.append(f"## Cross-References")
    cross_refs = analysis.get('cross_references', [])
    if cross_refs:
        for ref in cross_refs:
            lines.append(f"### Connection: {', '.join(ref.get('source_ids', []))}")
            if ref.get('headings'):
                lines.append(f"**Clauses:** {', '.join(ref.get('headings', []))}")
            lines.append(f"")
            if ref.get('connection_reason'):
                lines.append(f"**Why connected:** {ref.get('connection_reason')}")
                lines.append(f"")
            if ref.get('practical_implication'):
                lines.append(f"**Practical implication:** {ref.get('practical_implication')}")
                lines.append(f"")
            if ref.get('evidence_snippets'):
                lines.append(f"**Evidence:**")
                for snippet in ref.get('evidence_snippets', []):
                    lines.append(f"- {snippet}")
                lines.append(f"")
            lines.append(f"---")
            lines.append(f"")
    else:
        lines.append(f"*No cross-references identified.*")
        lines.append(f"")
    
    return "\n".join(lines)
