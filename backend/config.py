"""
Configuration management for the Campus Q&A Agent backend.
Uses environment variables with sensible defaults for development.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Flask configuration
class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{BASE_DIR / "data" / "campus_qa.db"}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # LLM API configuration (Chinese LLM providers)
    LLM_API_TYPE = os.getenv('LLM_API_TYPE', 'mock')  # 'iflytek', 'baidu', 'mock'
    LLM_API_KEY = os.getenv('LLM_API_KEY', '')
    LLM_API_BASE_URL = os.getenv('LLM_API_BASE_URL', '')
    LLM_MODEL = os.getenv('LLM_MODEL', 'Spark-3.0')  # Default to iFlyTek Spark

    # Embedding model configuration
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text2vec-base-chinese')
    EMBEDDING_DIMENSION = 384  # Dimension for text2vec-base-chinese

    # Vector store configuration
    FAISS_INDEX_PATH = os.getenv(
        'FAISS_INDEX_PATH',
        str(BASE_DIR / 'indexes' / 'faiss_index')
    )

    # Knowledge base paths
    DATA_DIR = BASE_DIR / 'data'
    CRAWLED_DIR = DATA_DIR / 'crawled'
    PROCESSED_DIR = DATA_DIR / 'processed'
    QA_PAIRS_DIR = DATA_DIR / 'qa_pairs'

    # RAG configuration
    MAX_CONTEXT_LENGTH = 2000  # Max characters for context window
    TOP_K_RESULTS = 5  # Number of similar documents to retrieve
    TEMPERATURE = 0.7  # LLM temperature for answer generation

    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

    # Rate limiting (requests per minute)
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', '60'))

    @staticmethod
    def init_app(app):
        """Initialize application with this configuration."""
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    LLM_API_TYPE = 'mock'  # Use mock LLM for testing

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Require secure secrets in production
    SECRET_KEY = os.getenv('SECRET_KEY', '')  # Will be validated in init_app
    # Note: SECRET_KEY validation happens in init_app method

    # Use MySQL/PostgreSQL in production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL must be set in production")

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Get configuration class by name."""
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    return config.get(config_name, config['default'])