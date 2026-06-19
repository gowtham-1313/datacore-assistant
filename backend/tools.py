# backend/tools.py
from sqlalchemy import create_engine, text
from typing import List, Dict, Any

# Connect to database
engine = create_engine('sqlite:///backend/data/datacore.db', echo=False)

# ============================================
# TOOL 1: Query Movie Data
# ============================================
def query_movie_data(genre: str = None, year: str = None) -> List[Dict]:
    """
    Get movie performance data including watch hours, ratings, and views.
    Use this for questions about top performing titles, movie comparisons, or genre performance.
    """
    query = """
    SELECT 
        m.movie_id,
        m.title,
        m.genre,
        m.rating,
        COUNT(w.activity_id) as total_views,
        SUM(w.watch_duration_min) as total_watch_minutes,
        AVG(w.completion_pct) as avg_completion_pct
    FROM movies m
    LEFT JOIN watch_activity w ON m.movie_id = w.movie_id
    WHERE 1=1
    """
    
    if genre:
        query += f" AND m.genre = '{genre}'"
    if year:
        query += f" AND m.release_date LIKE '{year}%'"
    
    query += " GROUP BY m.movie_id ORDER BY total_watch_minutes DESC LIMIT 20"
    
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()
        
    return [dict(zip(columns, row)) for row in rows]

# ============================================
# TOOL 2: Get Regional Stats
# ============================================
def get_regional_stats(city: str = None, month: str = None) -> List[Dict]:
    """
    Get regional engagement metrics like total views, growth percentage, and ratings.
    Use this for questions about cities, countries, or regional performance.
    """
    query = """
    SELECT 
        city,
        country,
        total_views,
        avg_rating,
        growth_pct,
        report_month
    FROM regional_performance
    WHERE 1=1
    """
    
    if city:
        query += f" AND city = '{city}'"
    if month:
        query += f" AND report_month = '{month}'"
    
    query += " ORDER BY total_views DESC LIMIT 20"
    
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()
        
    return [dict(zip(columns, row)) for row in rows]

# ============================================
# TOOL 3: Get Genre Trends
# ============================================
def get_genre_trends(month: str = None) -> List[Dict]:
    """
    Get aggregated genre performance data including total views and completion rates.
    Use this for questions about genre performance, trends, or comparisons.
    """
    query = """
    SELECT 
        m.genre,
        COUNT(w.activity_id) as total_views,
        AVG(w.completion_pct) as avg_completion,
        AVG(m.rating) as avg_rating
    FROM movies m
    JOIN watch_activity w ON m.movie_id = w.movie_id
    WHERE 1=1
    """
    
    if month:
        query += f" AND w.watch_date LIKE '{month}%'"
    
    query += " GROUP BY m.genre ORDER BY total_views DESC"
    
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()
        
    return [dict(zip(columns, row)) for row in rows]

# ============================================
# TOOL DEFINITIONS FOR THE LLM
# ============================================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "query_movie_data",
            "description": "Get movie performance data including watch hours, ratings, and views. Use this for questions about top performing titles, movie comparisons, or genre performance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "genre": {
                        "type": "string",
                        "description": "Filter by genre (Action, Drama, Comedy, Sci-Fi, Thriller, Romance, Adventure)",
                        "enum": ["Action", "Drama", "Comedy", "Sci-Fi", "Thriller", "Romance", "Adventure"]
                    },
                    "year": {
                        "type": "string",
                        "description": "Filter by release year (e.g., '2025')"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_regional_stats",
            "description": "Get regional engagement metrics like total views, growth percentage, and ratings for cities or countries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., 'New York')"
                    },
                    "month": {
                        "type": "string",
                        "description": "Month in YYYY-MM format (e.g., '2025-01')"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_genre_trends",
            "description": "Get aggregated genre performance data including total views and completion rates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "month": {
                        "type": "string",
                        "description": "Month in YYYY-MM format (e.g., '2025-01')"
                    }
                }
            }
        }
    }
]

# ============================================
# EXECUTE TOOL FUNCTION
# ============================================
def execute_tool(tool_name: str, parameters: Dict) -> Any:
    """Execute a tool with given parameters"""
    if tool_name == "query_movie_data":
        return query_movie_data(**parameters)
    elif tool_name == "get_regional_stats":
        return get_regional_stats(**parameters)
    elif tool_name == "get_genre_trends":
        return get_genre_trends(**parameters)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")
