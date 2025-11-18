"""
Configuration management for MCP Server
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for database and server settings"""
    
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables"""
        # Database configuration
        self.DB_HOST = os.getenv("SUPABASE_DB_HOST")
        self.DB_NAME = os.getenv("SUPABASE_DB_NAME", "postgres")
        self.DB_USER = os.getenv("SUPABASE_DB_USER")
        self.DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
        self.DB_PORT = os.getenv("SUPABASE_DB_PORT", "5432")
        
        # Supabase API (optional, for future use)
        self.SUPABASE_URL = os.getenv("REACT_APP_SUPABASE_URL")
        self.SUPABASE_ANON_KEY = os.getenv("REACT_APP_SUPABASE_ANON_KEY")
        
        # Server configuration
        self.SERVER_NAME = "sign-language-db"
        self.SERVER_VERSION = "0.1.0"
    
    @property
    def db_config(self) -> dict:
        """Return database configuration as dictionary"""
        return {
            'host': self.DB_HOST,
            'database': self.DB_NAME,
            'user': self.DB_USER,
            'password': self.DB_PASSWORD,
            'port': self.DB_PORT
        }
    
    def validate(self) -> bool:
        """Validate that all required configuration is present"""
        required = [
            self.DB_HOST,
            self.DB_NAME,
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_PORT
        ]
        
        if not all(required):
            missing = []
            if not self.DB_HOST:
                missing.append("SUPABASE_DB_HOST")
            if not self.DB_NAME:
                missing.append("SUPABASE_DB_NAME")
            if not self.DB_USER:
                missing.append("SUPABASE_DB_USER")
            if not self.DB_PASSWORD:
                missing.append("SUPABASE_DB_PASSWORD")
            if not self.DB_PORT:
                missing.append("SUPABASE_DB_PORT")
            
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True


# Global config instance
config = Config()

