# app.py - Main application file
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import datetime
from werkzeug.middleware.proxy_fix import ProxyFix

# Import blueprints
from routes.auth import auth_bp
from routes.dates import dates_bp, admin_dates_bp
from routes.users import users_bp

# Load environment variables
load_dotenv()

def create_app():
    """Factory pattern for creating the Flask application"""
    app = Flask(__name__)
    
    # Configure app
    app.config.from_mapping(
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
        JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(days=7),
        MONGO_URI=os.getenv("CONNECTION_STRING"),
        DEBUG=os.getenv("DEBUG_MODE", "False").lower() == "true"
    )
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv("ALLOWED_ORIGIN", ""), 
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Set up JWT
    jwt = JWTManager(app)
    
    # Handle proxy headers for proper IP detection
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dates_bp, url_prefix='/api/dates')
    app.register_blueprint(admin_dates_bp, url_prefix='/api/admin/dates')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    # Home route
    @app.route('/')
    def home():
        return "<h1>DentixPro API - Backend en Flask para el sistema de citas dentales</h1>"
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000"))
    )