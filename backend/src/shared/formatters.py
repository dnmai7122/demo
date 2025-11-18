"""
Formatting utilities for output display
"""

from typing import Dict, Any
from datetime import datetime


def format_date(date: datetime) -> str:
    """
    Format datetime to Vietnamese format
    
    Args:
        date: Datetime object
        
    Returns:
        Formatted date string
    """
    return date.strftime('%d/%m/%Y %H:%M')


def format_topic(topic: Dict[str, Any]) -> str:
    """
    Format topic information for display
    
    Args:
        topic: Topic dictionary
        
    Returns:
        Formatted topic string
    """
    result = f"📚 **{topic['name']}** (Code: {topic['code']})\n"
    result += f"   **Level:** {topic['level']}\n"
    if topic.get('description'):
        result += f"   **Mô tả:** {topic['description']}\n"
    result += f"   **Số bài học:** {topic.get('SL_lesson', 0)}\n"
    return result


def format_lesson(lesson: Dict[str, Any]) -> str:
    """
    Format lesson information for display
    
    Args:
        lesson: Lesson dictionary
        
    Returns:
        Formatted lesson string
    """
    result = f"📝 **{lesson['title']}**\n"
    result += f"   **ID:** {lesson.get('id', lesson.get('lesson_id'))}\n"
    if lesson.get('description'):
        result += f"   **Mô tả:** {lesson['description']}\n"
    result += f"   **Thứ tự:** {lesson.get('order_index', 'N/A')}\n"
    return result
