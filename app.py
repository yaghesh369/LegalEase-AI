import os
import streamlit as st
from dotenv import load_dotenv

from core.document_processor import DocumentProcessor
from core.summarizer import Summarizer
from core.risk_analyzer import RiskAnalyzer
from core.cross_reference import CrossReferenceAnalyzer
from core.qa import DocumentQA
from utils.validators import validate_pasted_text
from utils.export import export_analysis_to_markdown

load_dotenv()

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with modern animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #cbd5e1;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
        animation: fadeInDown 0.8s ease-out 0.1s backwards;
    }
    
    .disclaimer {
        background: linear-gradient(90deg, rgba(245, 158, 11, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        text-align: center;
        color: #fbbf24;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.8s ease-out 0.2s backwards;
    }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out 0.3s backwards;
    }
    
    .glass-card:hover {
        border-color: rgba(96, 165, 250, 0.4);
        box-shadow: 0 25px 50px rgba(59, 130, 246, 0.2);
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 41, 59, 0.4);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background: transparent;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.3);
        border-radius: 12px;
        color: #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
    }
    
    .stFileUploader > div {
        background: rgba(30, 41, 59, 0.6);
        border: 2px dashed rgba(148, 163, 184, 0.4);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #3b82f6;
        background: rgba(59, 130, 246, 0.1);
    }
    
    .stExpander {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .streamlit-expanderHeader {
        background: transparent;
        color: #e2e8f0;
        font-weight: 600;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">⚖️ LegalEase AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform complex legal documents into plain English with AI</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="disclaimer">⚠️ This is an educational tool, not a replacement for qualified legal advice</div>', unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📁 Upload PDF Document", "📝 Paste Legal Text"])
    
    doc_processor = DocumentProcessor()
    
    with tab1:
        st.markdown("### Upload Your Legal Document")
        st.markdown("Support for Terms & Conditions, Privacy Policies, Contracts and more")
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'], label_visibility="collapsed")
        if uploaded_file and st.button("🔍 Analyze PDF", key="analyze_pdf"):
            with st.spinner("✨ Extracting and processing your document..."):
                result = doc_processor.process_pdf(uploaded_file)
                if result.get('success'):
                    st.session_state.document = result
                    st.session_state.analysis_done = False
                    st.success("✅ Document processed successfully!")
                else:
                    st.error(f"❌ {result.get('error')}")
    
    with tab2:
        st.markdown("### Paste Legal Text")
        st.markdown("Copy and paste from any website or document")
        doc_title = st.text_input("Document Name (optional)", placeholder="e.g., Terms of Service")
        pasted_text = st.text_area("Legal Text", height=220, 
                                   placeholder="Paste your Terms & Conditions, Privacy Policy, or legal contract here...",
                                   label_visibility="collapsed")
        if st.button("🔍 Analyze Text", key="analyze_text"):
            valid, msg = validate_pasted_text(pasted_text)
            if not valid:
                st.error(f"❌ {msg}")
            else:
                with st.spinner("✨ Processing your text..."):
                    result = doc_processor.process_text(pasted_text, doc_title)
                    if result.get('success'):
                        st.session_state.document = result
                        st.session_state.analysis_done = False
                        st.success("✅ Text processed successfully!")
                    else:
                        st.error(f"❌ {result.get('error')}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis section
    if 'document' in st.session_state and st.session_state.document:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🧠 AI-Powered Analysis")
        
        if not st.session_state.get('analysis_done'):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Generate Complete Analysis", use_container_width=True):
                    doc = st.session_state.document
                    analysis = {}
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.markdown("**📊 Generating plain-English summary...**")
                        progress_bar.progress(25)
                        summarizer = Summarizer()
                        summary_result = summarizer.generate_summary(doc)
                        if summary_result.get('success'):
                            analysis['summary'] = summary_result['summary']
                        
                        status_text.markdown("**⚠️ Identifying potential risks...**")
                        progress_bar.progress(50)
                        risk_analyzer = RiskAnalyzer()
                        risk_result = risk_analyzer.analyze_risks(doc)
                        if risk_result.get('success'):
                            analysis['risks'] = risk_result['risks']
                        
                        status_text.markdown("**🔗 Finding clause relationships...**")
                        progress_bar.progress(75)
                        cross_ref = CrossReferenceAnalyzer()
                        cross_result = cross_ref.find_cross_references(doc)
                        if cross_result.get('success'):
                            analysis['cross_references'] = cross_result['cross_references']
                        
                        analysis['clauses'] = []
                        for section in doc.get('sections', [])[:20]:
                            analysis['clauses'].append({
                                "source_id": section['source_id'],
                                "heading": section.get('heading'),
                                "original_text_excerpt": section['text'][:250] + "..." if len(section['text']) > 250 else section['text'],
                                "page": section.get('page_number'),
                                "explanation": "AI analysis in progress context."
                            })
                        
                        progress_bar.progress(100)
                        status_text.markdown("**✅ Analysis Complete!**")
                        st.balloons()
                        
                        st.session_state.analysis = analysis
                        st.session_state.analysis_done = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
        else:
            analysis = st.session_state.get('analysis', {})
            
            tab_overview, tab_clauses, tab_risks, tab_cross, tab_qa = st.tabs([
                "📊 Overview", "📋 Key Clauses", "⚠️ Risks", "🔗 Cross-References", "💬 Ask AI"
            ])
            
            with tab_overview:
                st.markdown("### 📊 Document Overview")
                summary = analysis.get('summary', {})
                if summary:
                    for key, value in summary.items():
                        if value and value != "Not mentioned":
                            st.markdown(f"#### {key.replace('_', ' ').title()}")
                            if isinstance(value, list):
                                for item in value:
                                    st.markdown(f"- {item}")
                            else:
                                st.markdown(f"{value}")
                            st.markdown("---")
                else:
                    st.info("📭 No summary generated yet.")
            
            with tab_clauses:
                st.markdown("### 📋 Key Clauses Explorer")
                clauses = analysis.get('clauses', [])
                if clauses:
                    for clause in clauses:
                        with st.expander(f"📄 {clause['source_id']} • {clause.get('heading') or 'Clause'}"):
                            if clause.get('page'):
                                st.markdown(f"**📍 Page:** {clause['page']}")
                            st.markdown("**Original Text:**")
                            st.code(clause['original_text_excerpt'], language=None)
                            st.caption("ℹ️ AI-generated interpretations require verification by a qualified professional")
                else:
                    st.info("📭 No clauses available.")
            
            with tab_risks:
                st.markdown("### ⚠️ Potential Risks & Important Conditions")
                risks = analysis.get('risks', [])
                if risks:
                    for risk in risks:
                        severity_map = {"High": ("🔴", "#ef4444"), "Medium": ("🟡", "#f59e0b"), "Low": ("🟢", "#10b981")}
                        emoji, color = severity_map.get(risk.get('severity'), ("⚪", "#64748b"))
                        with st.expander(f"{emoji} [{risk.get('severity')}] {risk.get('title')}"):
                            col_r1, col_r2 = st.columns(2)
                            with col_r1:
                                st.markdown(f"**📌 Source:** {', '.join(risk.get('source_ids', []))}")
                            with col_r2:
                                if risk.get('page'):
                                    st.markdown(f"**📍 Page:** {risk.get('page')}")
                            st.markdown(f"**💡 Why it matters:** {risk.get('why_it_matters')}")
                            st.markdown("**📄 Supporting Evidence:**")
                            st.code(risk.get('excerpt'), language=None)
                            st.caption("⚖️ Distinction between actual wording and AI interpretation")
                else:
                    st.success("✅ No significant risks identified in this document")
            
            with tab_cross:
                st.markdown("### 🔗 Cross-References Between Clauses")
                cross_refs = analysis.get('cross_references', [])
                if cross_refs:
                    for ref in cross_refs:
                        with st.expander(f"🔗 Connected: {', '.join(ref.get('source_ids', []))}"):
                            st.markdown(f"**🔍 Connection:** {ref.get('connection_reason')}")
                            st.markdown(f"**💼 Practical Impact:** {ref.get('practical_implication')}")
                            st.markdown("**📋 Evidence:**")
                            for snippet in ref.get('evidence_snippets', []):
                                st.markdown(f"• {snippet}")
                else:
                    st.info("📭 No cross-references detected")
            
            with tab_qa:
                st.markdown("### 💬 Ask Questions About Your Document")
                st.markdown("Get answers grounded strictly in your document")
                
                question = st.text_input("Your Question", placeholder="e.g., Can this agreement renew automatically? How do I cancel?")
                if st.button("🎯 Get Answer", key="qa_btn"):
                    if question:
                        with st.spinner("🔍 Searching through document..."):
                            try:
                                qa = DocumentQA()
                                doc = st.session_state.document
                                result = qa.answer_question(doc, question)
                                if result.get('success'):
                                    qa_res = result['qa_result']
                                    st.markdown("#### 💡 Answer")
                                    st.markdown(f"{qa_res.get('answer')}")
                                    if qa_res.get('source_ids'):
                                        st.markdown(f"**📌 Sources:** {', '.join(qa_res['source_ids'])}")
                                    if qa_res.get('supporting_excerpts'):
                                        with st.expander("📄 View Supporting Excerpts"):
                                            for i, ex in enumerate(qa_res['supporting_excerpts']):
                                                st.code(ex, language=None)
                                                if i < len(qa_res['supporting_excerpts']) - 1:
                                                    st.markdown("---")
                                    if not qa_res.get('answer_found'):
                                        st.warning("⚠️ This response may not be fully grounded in the document")
                                else:
                                    st.error(f"❌ {result.get('error')}")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter a question")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📥 Export Analysis")
            doc = st.session_state.document
            markdown_content = export_analysis_to_markdown(analysis, doc)
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button(
                    label="📄 Download as Markdown",
                    data=markdown_content,
                    file_name=f"LegalEase_Analysis_{doc.get('title', 'document').replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col_d2:
                st.download_button(
                    label="📝 Download as Text",
                    data=markdown_content,
                    file_name=f"LegalEase_Analysis_{doc.get('title', 'document').replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
