# backend/main.py - COMPLETE WORKING VERSION
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import shutil
from pathlib import Path
import re  # <-- IMPORT RE MODULE

# Import our modules
from database import init_database
from tools import execute_tool, TOOLS, query_movie_data, get_regional_stats, get_genre_trends
from rag import search_pdf, index_pdf

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="DataCore Analytics Assistant",
    description="Internal analytics assistant for DataCore streaming company",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_database()

# ========== MODELS ==========
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, str]]
    session_id: str
    timestamp: str

# ========== STORE CHAT HISTORY ==========
chat_history = {}

# ========== GROQ API SETUP ==========
try:
    from groq import Groq
    groq_api_key = os.getenv("GROQ_API_KEY")
    client = None
    
    if not groq_api_key:
        print("⚠️ Warning: GROQ_API_KEY not found. Using demo mode.")
        print("⚠️ Get free API key from: https://console.groq.com/keys")
    else:
        client = Groq(api_key=groq_api_key)
        print("✅ Groq API client initialized")
except Exception as e:
    print(f"⚠️ Groq not installed or error: {e}")
    client = None

# ========== SYSTEM PROMPT ==========
SYSTEM_PROMPT = """You are DataCore Analytics Assistant. Answer questions about streaming data.

RULES:
1. Cite sources in every answer
2. Be specific with numbers
3. Use tools when needed
4. If you don't know, say so
"""

# ========== HELPER FUNCTIONS ==========
def call_llm(message: str, context: str = "", session_id: str = None) -> Dict:
    """Call LLM API or use demo mode"""
    
    # DEMO MODE - No API key
    if not client:
        return {
            "content": """📊 Based on the data I found:

**Top Performing Titles (Q1 2025):**
1. Stellar Run - 1,200,000 watch hours (Source: SQL Database)
2. Dark Orbit - 980,000 watch hours (Source: SQL Database)
3. Last Kingdom - 875,000 watch hours (Source: SQL Database)

**Genre Trends:**
- Sci-Fi grew 15% compared to Q4 2024
- Comedy performance is weak, down 8% (Source: quarterly_report_q1_2025.pdf)

📎 Sources: SQL Database, quarterly_report_q1_2025.pdf""",
            "tool_calls": []
        }
    
    # REAL API MODE
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if session_id and session_id in chat_history:
        messages = messages + chat_history[session_id][-10:]
    
    full_message = message
    if context:
        full_message = f"{message}\n\n[PDF Context: {context}]"
    
    messages.append({"role": "user", "content": full_message})
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=1000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content or ""
        tool_calls = []
        
        if response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                tool_calls.append({
                    "name": tool_call.function.name,
                    "parameters": json.loads(tool_call.function.arguments)
                })
        
        if session_id:
            if session_id not in chat_history:
                chat_history[session_id] = []
            chat_history[session_id].append({"role": "user", "content": message})
            chat_history[session_id].append({"role": "assistant", "content": content})
        
        return {"content": content, "tool_calls": tool_calls}
    
    except Exception as e:
        print(f"LLM API error: {e}")
        return {
            "content": f"Error: {str(e)}",
            "tool_calls": []
        }

# ========== ENDPOINT 1: POST /chat ==========
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        if not request.message or len(request.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        session_id = request.session_id or f"session_{int(datetime.now().timestamp())}"
        
        # Search PDFs for context
        pdf_results = search_pdf(request.message, top_k=3)
        pdf_context = ""
        sources = []
        
        for result in pdf_results:
            pdf_context += result['text'] + "\n\n"
            sources.append({
                "source": result['metadata']['source'],
                "type": "PDF",
                "chunk": str(result['metadata']['chunk_index'])
            })
        
        # ===== CHECK QUESTION TYPE AND CALL APPROPRIATE TOOL =====
        message_lower = request.message.lower()
        answer = ""
        
        # Tool 1: Movie data
        movie_keywords = ['title', 'movie', 'perform', 'watch hour', 'top', 'best', 'genre', 'rating']
        if any(word in message_lower for word in movie_keywords):
            try:
                genre = None
                genres = ['action', 'drama', 'comedy', 'sci-fi', 'thriller', 'romance', 'adventure']
                for g in genres:
                    if g in message_lower:
                        genre = g.title()
                        break
                
                year = None
                year_match = re.search(r'20\d{2}', message_lower)
                if year_match:
                    year = year_match.group()
                
                movie_data = query_movie_data(genre=genre, year=year)
                if movie_data:
                    sources.append({
                        "source": "SQL Database - Movies",
                        "type": "SQL",
                        "tool": "query_movie_data"
                    })
                    answer = "📊 **Movie Performance Data:**\n\n"
                    for i, movie in enumerate(movie_data[:10], 1):
                        watch_hours = movie.get('total_watch_minutes', 0)
                        watch_hours_str = f"{watch_hours:,}" if watch_hours else "N/A"
                        answer += f"{i}. **{movie['title']}** - {watch_hours_str} watch hours (Rating: {movie.get('rating', 'N/A')})\n"
                    answer += f"\n📎 **Source:** SQL Database"
                    
                    return ChatResponse(
                        answer=answer,
                        sources=sources,
                        session_id=session_id,
                        timestamp=datetime.now().isoformat()
                    )
            except Exception as e:
                print(f"Movie query error: {e}")
                answer = f"Error: {str(e)}"
        
        # Tool 2: Regional stats
        if not answer:
            region_keywords = ['city', 'region', 'country', 'growth', 'regional', 'viewer']
            if any(word in message_lower for word in region_keywords):
                try:
                    city = None
                    cities = ['new york', 'los angeles', 'chicago', 'london', 'paris', 'berlin', 'toronto', 'sydney']
                    for c in cities:
                        if c in message_lower:
                            city = c.title()
                            break
                    
                    month = None
                    month_match = re.search(r'20\d{2}-\d{2}', message_lower)
                    if month_match:
                        month = month_match.group()
                    
                    regional_data = get_regional_stats(city=city, month=month)
                    if regional_data:
                        sources.append({
                            "source": "SQL Database - Regions",
                            "type": "SQL",
                            "tool": "get_regional_stats"
                        })
                        answer = "🌍 **Regional Engagement Data:**\n\n"
                        for i, region in enumerate(regional_data[:10], 1):
                            growth = region.get('growth_pct', 0)
                            growth_str = f"+{growth}%" if growth > 0 else f"{growth}%"
                            answer += f"{i}. **{region['city']}** - {region['total_views']:,} views, {growth_str} growth\n"
                        answer += f"\n📎 **Source:** SQL Database"
                        
                        return ChatResponse(
                            answer=answer,
                            sources=sources,
                            session_id=session_id,
                            timestamp=datetime.now().isoformat()
                        )
                except Exception as e:
                    print(f"Regional query error: {e}")
                    answer = f"Error: {str(e)}"
        
        # Tool 3: Genre trends
        if not answer:
            genre_keywords = ['genre trend', 'genre performance', 'genre']
            if any(word in message_lower for word in genre_keywords):
                try:
                    genre_data = get_genre_trends()
                    if genre_data:
                        sources.append({
                            "source": "SQL Database - Genres",
                            "type": "SQL",
                            "tool": "get_genre_trends"
                        })
                        answer = "📈 **Genre Performance Data:**\n\n"
                        for genre in genre_data:
                            completion = genre.get('avg_completion', 0)
                            answer += f"• **{genre['genre']}** - {genre['total_views']:,} views, {completion:.0f}% completion rate\n"
                        answer += f"\n📎 **Source:** SQL Database"
                        
                        return ChatResponse(
                            answer=answer,
                            sources=sources,
                            session_id=session_id,
                            timestamp=datetime.now().isoformat()
                        )
                except Exception as e:
                    print(f"Genre query error: {e}")
                    answer = f"Error: {str(e)}"
        
        # If no tool matched, use PDF context
        if not answer:
            if pdf_context:
                pdf_sources = [s['source'] for s in sources if s['type'] == 'PDF']
                answer = f"📚 **Based on the PDF documents:**\n\n"
                lines = pdf_context.split('\n')
                important_lines = [line for line in lines if line.strip() and not line.startswith('---')]
                for line in important_lines[:15]:
                    answer += f"• {line}\n"
                if pdf_sources:
                    answer += f"\n📎 **Sources:** {', '.join(pdf_sources)}"
            else:
                answer = """🤔 I couldn't find specific data for your question. 

**Try asking about:**
• Movie performance ("Which titles performed best?")
• Regional engagement ("Which city had strongest growth?")
• Genre trends ("What are genre trends?")

**Example questions:**
• "Which titles performed best in Q1 2025?"
• "Compare Dark Orbit vs Last Kingdom"
• "Which city had strongest viewer growth?"
• "What explains weak comedy genre performance?"""
        
        if not sources:
            sources.append({
                "source": "General Knowledge",
                "type": "AI"
            })
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== ENDPOINT 2: GET /data/movies ==========
@app.get("/data/movies")
async def get_movies(
    genre: Optional[str] = Query(None, description="Filter by genre"),
    year: Optional[str] = Query(None, description="Filter by release year")
):
    try:
        valid_genres = ['Action', 'Drama', 'Comedy', 'Sci-Fi', 'Thriller', 'Romance', 'Adventure']
        if genre and genre not in valid_genres:
            raise HTTPException(status_code=400, detail=f"Invalid genre. Must be one of: {valid_genres}")
        
        if year and (not year.isdigit() or len(year) != 4):
            raise HTTPException(status_code=400, detail="Year must be 4 digits (e.g., 2025)")
        
        data = query_movie_data(genre=genre, year=year)
        return {
            "data": data,
            "filters": {"genre": genre, "year": year},
            "count": len(data)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching movie data: {str(e)}")

# ========== ENDPOINT 3: GET /data/regions ==========
@app.get("/data/regions")
async def get_regions(
    city: Optional[str] = Query(None, description="Filter by city"),
    month: Optional[str] = Query(None, description="Filter by month (YYYY-MM)")
):
    try:
        if month and len(month) != 7:
            raise HTTPException(status_code=400, detail="Month must be in YYYY-MM format (e.g., 2025-01)")
        
        data = get_regional_stats(city=city, month=month)
        return {
            "data": data,
            "filters": {"city": city, "month": month},
            "count": len(data)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching regional data: {str(e)}")

# ========== ENDPOINT 4: POST /ingest/pdf ==========
@app.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        upload_dir = Path("backend/data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        index_pdf(str(file_path))
        
        return {
            "message": f"Successfully ingested {file.filename}",
            "filename": file.filename
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting PDF: {str(e)}")

# ========== ENDPOINT 5: GET /history ==========
@app.get("/history")
async def get_history(
    session_id: str,
    limit: int = Query(10, description="Number of messages to return")
):
    try:
        if not session_id:
            raise HTTPException(status_code=400, detail="session_id is required")
        
        if limit > 100:
            raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
        
        history = chat_history.get(session_id, [])
        
        return {
            "session_id": session_id,
            "messages": history[-limit:],
            "count": len(history[-limit:]),
            "total_messages": len(history)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

# ========== HEALTH CHECK ==========
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# ========== ROOT ENDPOINT ==========
@app.get("/")
async def root():
    return {
        "name": "DataCore Analytics Assistant",
        "version": "1.0.0",
        "description": "Internal analytics assistant for DataCore streaming company",
        "endpoints": {
            "POST /chat": "Main chat endpoint",
            "GET /data/movies": "Get top movies by watch hours",
            "GET /data/regions": "Get regional engagement summary",
            "POST /ingest/pdf": "Upload and ingest PDF",
            "GET /history": "Get chat history",
            "GET /health": "Health check"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)