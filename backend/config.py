# config.py - Application configuration
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime

def configure_logging():
    """Set up application logging"""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure logging
    logging.basicConfig(
        level=log_level_map.get(log_level, logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create file handler for logging to file
    file_handler = RotatingFileHandler(
        'logs/dentixpro.log', 
        maxBytes=1024 * 1024 * 10,  # 10 MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # Get root logger and add handler
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    # Set SQLAlchemy logging to WARNING level to reduce noise
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    return root_logger

def get_config():
    """Get application configuration"""
    return {
        "HOST": os.getenv("HOST", "0.0.0.0"),
        "PORT": int(os.getenv("PORT", "5000")),
        "DEBUG": os.getenv("DEBUG_MODE", "False").lower() == "true",
        "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "change-this-in-production"),
        "JWT_ACCESS_TOKEN_EXPIRES": datetime.timedelta(days=7),
        "CONNECTION_STRING": os.getenv("CONNECTION_STRING"),
        "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS", "").split(","),
    }