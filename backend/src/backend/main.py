#!/usr/bin/env python3
"""
FastAPI Backend Server for Sign Language Database
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
from pathlib import Path
import os

# Add src to Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from shared.database import DatabaseManager
from shared.hybrid_search import get_search_service, initialize_search_service

# Initialize FastAPI app
app = FastAPI(
    title="Sign Language Learning API",
    description="API for managing sign language learning content",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database manager
db_manager = DatabaseManager()


# Request/Response models
class SearchRequest(BaseModel):
    """Request model for hybrid search"""
    query: str
    top_k: Optional[int] = 3


# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sign Language Learning API",
        "version": "1.0.0",
        "endpoints": {
            "topics": "/api/topics",
            "lessons_by_topic": "/api/topics/{topic_id}/lessons",
            "all_lessons": "/api/lessons"
        }
    }


@app.get("/api/topics")
async def get_all_topics():
    """Get all topics from database"""
    try:
        print("Fetching topics from database...")
        topics = db_manager.get_all_topics()
        print(f"Found {len(topics) if topics else 0} topics")
        
        # Convert to list if needed
        if topics is None:
            topics = []
        
        return {"success": True, "data": topics}
    except Exception as e:
        print(f"Error fetching topics: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/topics/search")
async def search_topics(query: str):
    """Search topics by name"""
    try:
        print(f"Searching topics with query: {query}")
        all_topics = db_manager.get_all_topics()
        
        if not all_topics:
            return {"success": True, "data": []}
        
        # Filter topics by name (case-insensitive)
        query_lower = query.lower()
        filtered_topics = [
            topic for topic in all_topics 
            if query_lower in topic.get('name', '').lower()
        ]
        
        print(f"Found {len(filtered_topics)} matching topics")
        return {"success": True, "data": filtered_topics}
    except Exception as e:
        print(f"Error searching topics: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@app.get("/api/topics/{topic_id}/lessons")
async def get_lessons_by_topic(topic_id: int):
    """Get all lessons for a specific topic"""
    try:
        print(f"Fetching lessons for topic {topic_id}...")
        lessons = db_manager.get_lessons_by_topic(topic_id)
        print(f"Found {len(lessons) if lessons else 0} lessons")
        
        # Convert to list if needed
        if lessons is None:
            lessons = []
        
        return {"success": True, "data": lessons}
    except Exception as e:
        print(f"Error fetching lessons: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/lessons")
async def get_all_lessons():
    """Get all lessons from database"""
    try:
        print("Fetching all lessons from database...")
        lessons = db_manager.get_all_lessons()
        print(f"Found {len(lessons) if lessons else 0} lessons")
        
        # Convert to list if needed
        if lessons is None:
            lessons = []
        
        return {"success": True, "data": lessons}
    except Exception as e:
        print(f"Error fetching lessons: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Sign Language Learning API"}


@app.post("/api/search/units")
async def search_units(request: SearchRequest):
    """
    Hybrid search for units by description
    Combines semantic search (Gemini embeddings) and keyword search (BM25)
    """
    try:
        # Get search service
        search_service = get_search_service()
        
        # Initialize if not already done
        if not search_service.is_initialized:
            print("Initializing search service...")
            units = db_manager.get_all_units()
            initialize_search_service(units)
        
        # Perform hybrid search
        results = search_service.search(
            query=request.query,
            top_k=request.top_k
        )
        
        return {
            "success": True,
            "query": request.query,
            "count": len(results),
            "data": results
        }
    except Exception as e:
        print(f"Error in hybrid search: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Initialize search service on startup"""
    try:
        print("🚀 Starting up application...")
        # Pre-load units for search
        units = db_manager.get_all_units()
        if units:
            print(f"Loading {len(units)} units for search indexing...")
            initialize_search_service(units)
            print("✅ Search service initialized successfully")
        else:
            print("⚠️ No units found - search service will initialize on first request")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize search service: {str(e)}")
        print("Search service will initialize on first request")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

