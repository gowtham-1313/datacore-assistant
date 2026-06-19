+-----------------------------------------------------+
|                                                     |
|           DATA FLOW DIAGRAM                         |
|                                                     |
+-----------------------------------------------------+

     +-------------------+
     |                   |
     |    USER TYPES     |
     |    A QUESTION     |
     |                   |
     +--------+----------+
              |
              v
     +--------+----------+
     |                   |
     |    FRONTEND       |
     |    (HTML/JS)      |
     |                   |
     +--------+----------+
              |
              v
     +--------+----------+
     |                   |
     |   FASTAPI         |
     |   BACKEND         |
     |                   |
     +--------+----------+
              |
     +--------+---------+
     |                  |
     |    /chat         |
     |    ENDPOINT      |
     |                  |
     +--------+---------+
              |
    +---------+-----------+
    |                     |
    |   RAG SEARCH        |
    |   IN PDF FILES      |
    |                     |
    +---------+-----------+
              |
    +---------+-----------+
    |                     |
    |   LLM DECIDES       |
    |   WHICH TOOL        |
    |   TO USE            |
    |                     |
    +---------+-----------+
              |
     +--------+-----------+
     |                    |
     |    TOOLS RUN       |
     |    ON SQLITE DB    |
     |                    |
     +--------+-----------+
              |
     +--------+-----------+
     |                    |
     |   ANSWER WITH      |
     |   SOURCES          |
     |   RETURNED         |
     |                    |
     +--------+-----------+

+-----------------------------------------------------+
|                                                     |
|           COMPONENTS EXPLAINED                      |
|                                                     |
+-----------------------------------------------------+

    1. FRONTEND (HTML/CSS/JS)
       - User types question
       - Shows chat history
       - Displays source badges
       - Shows genre chart

    2. BACKEND (FastAPI)
       - Handles 5 endpoints
       - Processes chat requests
       - Manages data access

    3. RAG PIPELINE
       - Loads PDF documents
       - Chunks text (400 words with overlap)
       - Creates embeddings
       - Searches for relevant content

    4. TOOLS (3 tools)
       - query_movie_data
       - get_regional_stats
       - get_genre_trends

    5. DATA STORES
       - SQLite: Movies, Viewers, Activity, Reviews, Marketing, Regional
       - ChromaDB: PDF embeddings and metadata

    6. LLM (Groq API)
       - Understands user question
       - Decides which tool to call
       - Generates final answer

+-----------------------------------------------------+
|                                                     |
|           TECHNOLOGIES USED                         |
|                                                     |
+-----------------------------------------------------+

    Python 3.10          - Programming Language
    FastAPI              - Backend Framework
    SQLite               - Database
    ChromaDB             - Vector Store
    Sentence Transformers - Embeddings
    PyPDF2               - PDF Processing
    Groq API             - LLM (Llama 3.3 70B)
    HTML/CSS/JS          - Frontend
    Chart.js             - Charts

+-----------------------------------------------------+
|                                                     |
|           HOW IT WORKS (STEP BY STEP)               |
|                                                     |
+-----------------------------------------------------+

    STEP 1: User asks: "Which titles performed best?"
           ↓
    STEP 2: Frontend sends to /chat endpoint
           ↓
    STEP 3: Backend searches PDFs using RAG
           ↓
    STEP 4: LLM decides to use query_movie_data tool
           ↓
    STEP 5: Tool queries SQLite database
           ↓
    STEP 6: Results formatted with sources
           ↓
    STEP 7: Answer sent back to user
           ↓
    STEP 8: Frontend shows answer + source badges

+-----------------------------------------------------+
|                                                     |
|           SOURCE ATTRIBUTION SYSTEM                  |
|                                                     |
+-----------------------------------------------------+

    SQL Query           → "Source: SQL Database"
    PDF Search          → "Source: quarterly_report.pdf"
    No Data Found       → "Source: General Knowledge"

    Users always know WHERE the data came from!

+-----------------------------------------------------+
|                                                     |
|           PROJECT STRUCTURE                          |
|                                                     |
+-----------------------------------------------------+

    datacore_assistant/
    ├── backend/
    │   ├── main.py           # FastAPI application
    │   ├── database.py       # SQLite setup
    │   ├── tools.py          # 3 tools for LLM
    │   ├── rag.py            # PDF search pipeline
    │   └── data/
    │       ├── csv_files/    # 6 CSV files
    │       └── pdf_files/    # 2 PDF reports
    ├── frontend/
    │   └── index.html        # Single page UI
    ├── .env                  # API keys (not uploaded)
    ├── .env.example          # Template for keys
    └── README.md             # Project documentation