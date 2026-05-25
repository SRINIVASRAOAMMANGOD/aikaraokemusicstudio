import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    
    # File upload settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'ogg', 'm4a', 'aac'}
    
    # Database settings
    DATABASE_FILE = os.environ.get('DATABASE_FILE', 'karaoke_studio.db')
    
    # Demucs settings
    DEFAULT_MODEL = os.environ.get('DEMUCS_MODEL', 'htdemucs')
    AVAILABLE_MODELS = [
        'htdemucs',
        'htdemucs_ft',
        'htdemucs_6s',
        'mdx_extra',
        'mdx_extra_q'
    ]
    
    # Audio processing settings
    DEFAULT_SAMPLE_RATE = 48000
    DEFAULT_BUFFER_SIZE = 512
    TORCH_NUM_THREADS = int(os.environ.get('TORCH_NUM_THREADS', 4))
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME = 'aikaraoke_session'
    
    # API settings
    API_MAX_REQUESTS_PER_MINUTE = 60
    
    # Feature flags
    ENABLE_YOUTUBE_DOWNLOAD = os.environ.get('ENABLE_YOUTUBE_DOWNLOAD', 'true').lower() == 'true'
    ENABLE_AI_ANALYSIS = os.environ.get('ENABLE_AI_ANALYSIS', 'true').lower() == 'true'
    ENABLE_CLOUD_STORAGE = os.environ.get('ENABLE_CLOUD_STORAGE', 'false').lower() == 'true'
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'info').upper()


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration - strict requirements"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    def __init__(self):
        super().__init__()
        # Enforce SECRET_KEY in production
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key or len(secret_key) < 32:
            raise ValueError(
                "CRITICAL: SECRET_KEY environment variable must be set in production "
                "and be at least 32 characters long. "
                "Generate one: python3 -c \"import secrets; print(secrets.token_urlsafe(32))\""
            )
        self.SECRET_KEY = secret_key


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Use separate test database
    DATABASE_FILE = 'test_karaoke_studio.db'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Faster password hashing for tests
    BCRYPT_LOG_ROUNDS = 4


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration by name"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    config_class = config.get(config_name, config['default'])
    
    # Instantiate config if it's ProductionConfig (needs validation)
    if config_class == ProductionConfig:
        return config_class()
    
    return config_class()
