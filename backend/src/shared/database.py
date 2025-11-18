"""
Database connection and management utilities using Supabase REST API
"""

import requests
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseManager:
    """Database manager using Supabase REST API"""
    
    def __init__(self):
        self.supabase_url = os.getenv("REACT_APP_SUPABASE_URL")
        self.supabase_key = os.getenv("REACT_APP_SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Missing REACT_APP_SUPABASE_URL or REACT_APP_SUPABASE_ANON_KEY environment variables")
        
        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, params: dict = None) -> List[Dict[str, Any]]:
        """
        Make a request to Supabase REST API
        
        Args:
            endpoint: The table/endpoint name
            params: Query parameters
            
        Returns:
            List of dictionaries with results
        """
        url = f"{self.supabase_url}/rest/v1/{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Database error: {str(e)}")
    
    # Lesson-specific methods
    def get_lessons_by_topic(self, topic_id: int) -> List[Dict[str, Any]]:
        """Get all lessons for a specific topic"""
        params = {
            "topic_id": f"eq.{topic_id}",
            "select": "lesson_id,topic_id,title,description,order_index,slug",
            "order": "order_index.asc,lesson_id.asc"
        }
        lessons = self._make_request("lesson", params=params)
        
        # Rename lesson_id to id for consistency
        for lesson in lessons:
            if 'lesson_id' in lesson:
                lesson['id'] = lesson['lesson_id']
        
        return lessons
    
    def get_all_lessons(self) -> List[Dict[str, Any]]:
        """Get all lessons from database"""
        params = {
            "select": "lesson_id,topic_id,title,description,order_index,slug",
            "order": "topic_id.asc,order_index.asc,lesson_id.asc"
        }
        lessons = self._make_request("lesson", params=params)
        
        # Rename lesson_id to id for consistency
        for lesson in lessons:
            if 'lesson_id' in lesson:
                lesson['id'] = lesson['lesson_id']
        
        return lessons
    
    # Topic-specific methods
    def get_all_topics(self) -> List[Dict[str, Any]]:
        """Get all topics from database with lesson count"""
        # Get all active topics
        params = {
            "is_active": "eq.true",
            "select": "topic_id,name,code,description,level,cover_image_url,cover_video_url,order_index,is_active",
            "order": "order_index.asc,topic_id.asc"
        }
        topics = self._make_request("topic", params=params)
        
        # Get all lessons to count them
        lesson_params = {
            "select": "topic_id"
        }
        lessons = self._make_request("lesson", params=lesson_params)
        
        # Count lessons per topic
        lesson_counts = {}
        for lesson in lessons:
            topic_id = lesson.get('topic_id')
            if topic_id:
                lesson_counts[topic_id] = lesson_counts.get(topic_id, 0) + 1
        
        # Add lesson count and rename topic_id to id
        for topic in topics:
            topic_id = topic.get('topic_id')
            topic['id'] = topic_id
            topic['SL_lesson'] = lesson_counts.get(topic_id, 0)
        
        return topics
    
    # Unit-specific methods
    def get_all_units(self) -> List[Dict[str, Any]]:
        """Get all units from database"""
        params = {
            "select": "unit_id,lesson_id,type,text,description,code,order_index,image_url,video_url",
            "order": "lesson_id.asc,order_index.asc"
        }
        units = self._make_request("unit", params=params)
        
        # Rename unit_id to id for consistency
        for unit in units:
            if 'unit_id' in unit:
                unit['id'] = unit['unit_id']
        
        return units
