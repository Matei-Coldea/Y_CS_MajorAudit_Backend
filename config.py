"""Configuration management for the Yale Degree Audit application."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if not in production
if os.environ.get('FLASK_ENV') != 'production':
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
    PORT = int(os.environ.get("PORT", "5000"))
    
    @staticmethod
    def validate():
        """Validate that all required configuration values are present."""
        missing_vars = []
        if not Config.SUPABASE_URL:
            missing_vars.append("SUPABASE_URL")
        if not Config.SUPABASE_KEY:
            missing_vars.append("SUPABASE_KEY")
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    def __init__(self):
        if not self.SECRET_KEY or self.SECRET_KEY == "dev-key-not-for-production":
            raise ValueError("Production environment requires a secure SECRET_KEY")


# Dictionary of available configurations
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# Get the active configuration based on the environment
env = os.environ.get('FLASK_ENV', 'development')
active_config = config_by_name.get(env)

if active_config is None:
    raise ValueError(f"Invalid FLASK_ENV value: {env}. Must be one of: {', '.join(config_by_name.keys())}")
