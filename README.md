# 🎬 DataCore Analytics Assistant

An AI-powered analytics assistant built for **DataCore**, a fictional streaming entertainment platform. The system enables users to explore movie performance, audience engagement, regional trends, and business insights through natural language conversations backed by structured data and document retrieval.

---

## ✨ Key Features

* Conversational analytics interface with source attribution
* Retrieval-Augmented Generation (RAG) using PDF documents
* SQL-powered business intelligence tools
* Regional and genre performance analysis
* Interactive data visualizations
* Source-backed responses for transparency and trust

---

## 🏗️ System Architecture

```text
User
  │
  ▼
Frontend (HTML/CSS/JS)
  │
  ▼
FastAPI Backend
  │
  ├── Analytics Tools
  ├── SQLite Database
  └── ChromaDB Vector Store
          │
          ▼
   LLM Response + Sources
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* Conda (recommended)
* Groq API Key

### Installation

#### 1. Create a virtual environment

```bash
conda create -n datacore python=3.10
conda activate datacore
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure environment variables

```bash
cp .env.example .env
```

Add your API key:

```env
GROQ_API_KEY=your_api_key_here
```

#### 4. Generate sample data and build the vector index

```bash
python backend/create_pdfs.py
python backend/rag.py
```

#### 5. Start the application

```bash
python backend/main.py
```

Open:

```text
frontend/index.html
```

in your browser.

---

## 📊 Data Sources

### Structured Data

The assistant uses multiple business datasets including:

* Movies
* Viewers
* Watch Activity
* Reviews
* Marketing Spend
* Regional Performance

### Unstructured Documents

* Quarterly Business Reports
* Marketing Campaign Analysis Reports

These documents are indexed and retrieved through the RAG pipeline to provide contextual answers.

---

## 🛠️ Analytics Tools

| Tool                 | Purpose                                |
| -------------------- | -------------------------------------- |
| `query_movie_data`   | Retrieve movie performance metrics     |
| `get_regional_stats` | Analyze regional engagement and growth |
| `get_genre_trends`   | Explore genre performance trends       |

---

## 🔌 API Endpoints

| Endpoint        | Method | Description                            |
| --------------- | ------ | -------------------------------------- |
| `/chat`         | POST   | Main conversational analytics endpoint |
| `/data/movies`  | GET    | Movie insights with filtering options  |
| `/data/regions` | GET    | Regional performance analytics         |
| `/ingest/pdf`   | POST   | Upload and index PDF documents         |
| `/history`      | GET    | Retrieve session chat history          |
| `/health`       | GET    | Service health check                   |

---

## 💬 Example Questions

* Which titles generated the highest watch hours in Q1 2025?
* Why is *Stellar Run* trending this month?
* Compare audience engagement between *Dark Orbit* and *Last Kingdom*.
* Which region experienced the strongest viewer growth?
* What factors are impacting comedy genre performance?
* What strategic recommendations can improve next quarter's performance?

---

## 🧰 Technology Stack

### Backend

* FastAPI
* Python 3.10
* SQLAlchemy

### Data Layer

* SQLite
* ChromaDB

### AI & Machine Learning

* Groq (Llama 3.3 70B)
* Sentence Transformers (`all-MiniLM-L6-v2`)
* Retrieval-Augmented Generation (RAG)

### Frontend

* HTML
* CSS
* JavaScript
* Chart.js

### Document Processing

* PyPDF2

---

## 📁 Project Structure

```text
datacore_assistant/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── tools.py
│   ├── rag.py
│   └── create_pdfs.py
│
├── frontend/
│   └── index.html
│
├── .env.example
├── requirements.txt
├── README.md
└── ARCHITECTURE.md
```

---

## ⚖️ Design Decisions

### Assumptions

* Data is generated for demonstration purposes.
* Users provide a valid Groq API key.
* Application runs locally.
* PDF documents are text-extractable.
* SQLite is sufficient for the expected data volume.

### Tradeoffs

* In-memory chat history storage.
* Static frontend implementation.
* Local ChromaDB persistence.
* Groq selected for cost-effective inference.

---

## 🚧 Current Limitations

* Large PDF files require longer indexing times.
* Chat history is not persisted across server restarts.
* No streaming responses.
* No authentication or role-based access control.
* Not optimized for production-scale deployment.

---

## 👨‍💻 Author

**Gowtham Kadimisetty**

---

## 📄 License

This project was developed for educational and portfolio purposes.
