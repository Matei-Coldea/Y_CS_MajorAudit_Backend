"""Configuration management for the Yale Degree Audit application."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    
    # Supabase configuration
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    
    # Flask configuration
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-not-for-production")
    
    # API configuration
    PORT = int(os.environ.get("PORT", "5001").split('#')[0].strip())
    
    @staticmethod
    def validate():
        """Validate that all required configuration values are present."""
        if not Config.SUPABASE_URL:
            raise ValueError("SUPABASE_URL environment variable is required")
        if not Config.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY environment variable is required")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    # Production-specific settings would go here
    pass


# Dictionary of available configurations
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# Get the active configuration based on the environment
active_config = config_by_name.get(os.environ.get('FLASK_ENV', 'development'))
