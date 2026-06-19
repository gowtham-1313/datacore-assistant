# DataCore Analytics Assistant

An internal analytics assistant for DataCore streaming company. This AI chatbot answers questions about movie performance, regional engagement, and genre trends with source citation.

## Features
- Chat interface with source badges
- RAG pipeline for PDF search
- Tool-based data access (SQL database)
- Genre performance charts with filters

## Setup
1. Create conda environment: `conda create -n datacore python=3.10`
2. Activate: `conda activate datacore`
3. Install: `pip install -r requirements.txt`
4. Add GROQ_API_KEY to .env file
5. Run: `python backend/main.py`
6. Open: `frontend/index.html`

## Technologies
- Backend: FastAPI, Python 3.10
- Database: SQLite (SQLAlchemy)
- Vector DB: ChromaDB
- LLM: Groq (Llama 3.3 70B)
- Frontend: HTML, CSS, JavaScript, Chart.js
- RAG: Sentence Transformers, PyPDF2

## Example Questions
- "Which titles performed best in Q1 2025?"
- "Which city had strongest viewer growth?"
- "What are genre trends?"

## Author
[Your Name]

## License
Created for WT Softech Technical Assessment