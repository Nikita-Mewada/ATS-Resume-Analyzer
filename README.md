# ATS Resume Analyzer

Upload a resume (PDF) and paste a job description to get an ATS-style match score
with skill gaps and improvement suggestions.

## Features
- PDF text extraction (PyMuPDF)
- Skill matching with a custom regex that handles C++, C#, Node.js
- Keyword matching with spaCy lemmatization
- Semantic similarity using sentence-transformers (all-MiniLM-L6-v2)
- Weighted ATS score: 40% skills + 20% keywords + 40% semantic similarity
- Interactive charts (Plotly) and analysis history (SQLite)

## Tech Stack
Python, Streamlit, PyMuPDF, spaCy, scikit-learn, sentence-transformers, pandas, SQLite

## How It Works
Resume PDF → text extraction → cleaning + NLP → skill / keyword / semantic scores → weighted ATS score → saved to SQLite

## Setup
```bash
git clone https://github.com/<your-username>/ATS-Resume-Analyzer.git
cd ATS-Resume-Analyzer
python -m venv venv
venv\Scripts\activate        # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

## Limitations
- Works only on text-based PDFs (no OCR for scanned resumes)
- Skill list is a fixed CSV
- Semantic model reads about 256 tokens, so long documents are truncated

## Future Improvements
OCR support, text chunking, larger skill taxonomy, FastAPI backend
