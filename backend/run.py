# run.py - Application entry point
from app import create_app
from config import configure_logging, get_config

# Configure logging
logger = configure_logging()

# Create application instance
app = create_app()

if __name__ == "__main__":
    # Get configuration
    config = get_config()
    
    # Log startup information
    logger.info(f"Starting DentixPro API on {config['HOST']}:{config['PORT']}")
    logger.info(f"Debug mode: {config['DEBUG']}")
    
    # Run application
    app.run(
        host=config["HOST"],
        port=config["PORT"],
        debug=config["DEBUG"]
    )