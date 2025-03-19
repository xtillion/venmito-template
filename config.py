"""Application configuration."""

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = "dev-key-change-in-production"

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True

class ProductionConfig(Config):
    """Production configuration."""
    SECRET_KEY = "production-key-to-be-set-securely"
