# CampusIntelli Database Configuration
# This file contains database configuration for future use
# Currently using local JSON storage - DB connection is commented out

import os

class DatabaseConfig:
    """Database configuration for different environments"""
    
    # PostgreSQL connection string (for production)
    # Format: postgresql://user:password@host:port/database
    POSTGRES_URL = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/campusintelli')
    
    # SQLite for local development
    SQLITE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'campusintelli.db')
    SQLITE_URL = f'sqlite:///{SQLITE_PATH}'
    
    # Supabase configuration (for future cloud deployment)
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
    
    # Current active database URL
    # Change this to switch between databases
    ACTIVE_DB = SQLITE_URL
    
    # SQLAlchemy engine options
    ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'echo': False  # Set True for SQL debugging
    }
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Get the active database connection string"""
        return cls.ACTIVE_DB
    
    @classmethod
    def is_postgres(cls) -> bool:
        """Check if using PostgreSQL"""
        return cls.ACTIVE_DB.startswith('postgresql')
    
    @classmethod
    def is_sqlite(cls) -> bool:
        """Check if using SQLite"""
        return cls.ACTIVE_DB.startswith('sqlite')
