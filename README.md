# LegalEase AI

An AI-powered Streamlit application that simplifies complex legal documents into easy-to-understand summaries using Google Gemini API.

## Features

- **Upload PDF** - Extract and analyze PDF legal documents (with page number preservation)
- **Paste Text** - Paste Terms & Conditions, Privacy Policies, or any legal text directly
- **Plain-English Summary** - Get structured summaries in simple language
- **Clause Explorer** - Browse and understand individual clauses with source references
- **Risk Analysis** - Identify potentially unfavorable provisions with severity levels
- **Cross-References** - Discover connections between related clauses
- **Document Q&A** - Ask questions and get answers grounded only in your document
- **Download Results** - Export analysis as Markdown or Text

## Technology Stack

- Python 3.9–3.13 (Python 3.14 is not currently supported by the installed PyMuPDF binary)
- Streamlit
- Google Gemini API (google-genai)
- PyMuPDF (pymupdf)
- python-dotenv
- pytest

## Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/apikey))

## Setup (Windows PowerShell)

### 1. Create and activate virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root based on `.env.example`:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

## Running the Application

From the project root, use the virtual environment's Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Keep this PowerShell window open while using the app. The server is running as long as
the command is still active and the terminal has not returned to the `PS ...>` prompt.
Open `http://127.0.0.1:8501` in your browser.

If the virtual environment is activated, this shorter command is equivalent:

```powershell
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

### Troubleshooting startup

- If PowerShell immediately returns to the prompt, run the command from the project
  root and use `python -m streamlit` rather than a globally installed `streamlit`.
- If port 8501 is already in use, start on another port:

  ```powershell
  .\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502
  ```

- Do not start the app with `python app.py`; Streamlit applications must be started
  with `python -m streamlit run app.py`.
- If the terminal prints the URL and then closes, check your Python version with
  `python --version`. Python 3.14 can crash while loading PyMuPDF on Windows.
  Install Python 3.13, recreate `.venv`, and reinstall dependencies:

  ```powershell
  py -3.13 -m venv .venv
  .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  .\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
  ```

## Running Tests

```powershell
python -m pytest -v
```

## Example Test Documents

Use these to quickly test both modes of the app:

### For Pasting Text (Terms & Conditions / Policies)

| Document | Link | Notes |
| --- | --- | --- |
| GitHub Terms of Service | [https://docs.github.com/en/site-policy/github-terms/github-terms-of-service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) | Clean and structured. Great for testing summary, risks, and Q&A. |
| Google Terms of Service | [https://policies.google.com/terms](https://policies.google.com/terms) | Good for spotting renewal, liability, and changes to terms. |
| Google Privacy Policy | [https://policies.google.com/privacy](https://policies.google.com/privacy) | Ideal for testing the "Data collection & privacy" section. |

### For Uploading PDF

| Document | Link | Notes |
| --- | --- | --- |
| W3C Software Notice & License | [https://www.w3.org/Consortium/Legal/2002/copyright-software-20021231.pdf](https://www.w3.org/Consortium/Legal/2002/copyright-software-20021231.pdf) | Text-based PDF. PyMuPDF extracts well with page numbers preserved. |
| Creative Commons Attribution 4.0 Legal Code | [https://creativecommons.org/licenses/by/4.0/legalcode.pdf](https://creativecommons.org/licenses/by/4.0/legalcode.pdf) | Another clean text-based PDF. Good to test clause splitting and page references. |

> **Note:** Avoid scanned/image-only PDFs. The app will show a message stating that OCR is required, which is outside the scope of this project.

## Usage

### PDF Upload
1. Go to "Upload PDF" tab
2. Upload your legal document
3. Click "Analyze PDF"
4. Click "Generate Full Analysis" to run AI analysis

### Paste Text
1. Go to "Paste Text" tab
2. Optionally add a document title
3. Paste your legal text
4. Click "Analyze Text"
5. Click "Generate Full Analysis" to run AI analysis

## Known Limitations

- **Scanned PDFs**: PDFs with only images (scanned documents) have no extractable text. OCR is not included in this version.
- **AI Interpretations**: All AI-generated content may need verification by a qualified legal professional.
- **Document Grounding**: The app tries to answer only from the document, but AI can occasionally misinterpret.
- **Context Limits**: Very long documents are truncated for analysis to fit model limits.
- **Not Legal Advice**: This is an educational tool, not a substitute for legal counsel.

## Disclaimer

This tool is for educational purposes only. It does not provide legal advice, create an attorney-client relationship, or replace consultation with a qualified lawyer.
