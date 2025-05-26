# conftest.py - Configuración de pytest
import pytest
import mongomock
from unittest.mock import patch
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from datetime import datetime, timedelta

# Importar tu aplicación y blueprints
from app import create_app
from routes.auth import auth_bp
from routes.dates import dates_bp, admin_dates_bp
from routes.users import users_bp  # Asegúrate de que existe
from db import Database

@pytest.fixture
def mock_db():
    """Mock de MongoDB usando mongomock"""
    with patch.object(Database, 'get_instance') as mock_instance:
        # Crear cliente mock de MongoDB
        mock_client = mongomock.MongoClient()
        mock_database = mock_client.test_database
        
        # Configurar el mock para retornar colecciones mock
        mock_db_instance = mock_instance.return_value
        mock_db_instance.get_collection.side_effect = lambda name: mock_database[name]
        
        yield mock_db_instance

@pytest.fixture
def app(mock_db):
    """Crear aplicación Flask para testing"""
    # Crear nueva instancia de Flask para testing
    test_app = Flask(__name__)
    test_app.config.update({
        "TESTING": True,
        "JWT_SECRET_KEY": "test-secret-key",
        "JWT_ACCESS_TOKEN_EXPIRES": timedelta(hours=1),
        "MONGO_URI": "mongodb://localhost:27017/test_db"
    })
    
    # Configurar JWT
    jwt = JWTManager(test_app)
    
    # Registrar blueprints
    test_app.register_blueprint(auth_bp, url_prefix='/auth')
    test_app.register_blueprint(dates_bp, url_prefix='/dates')
    test_app.register_blueprint(admin_dates_bp, url_prefix='/admin/dates')
    test_app.register_blueprint(users_bp, url_prefix='/users')
    
    return test_app

@pytest.fixture
def client(app):
    """Cliente de testing Flask"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner de comandos CLI"""
    return app.test_cli_runner()

@pytest.fixture
def sample_user_data():
    """Datos de usuario de ejemplo para testing"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123",
        "rol": "user"
    }

@pytest.fixture
def sample_admin_data():
    """Datos de admin de ejemplo para testing"""
    return {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "adminpassword123",
        "rol": "admin"
    }

@pytest.fixture
def test_user(mock_db, sample_user_data):
    """Crea un usuario de prueba en la base de datos mock"""
    from werkzeug.security import generate_password_hash
    
    user_data = sample_user_data.copy()
    user_data['password'] = generate_password_hash(user_data['password'])
    user_data['_id'] = '507f1f77bcf86cd799439011'  # ObjectId mock
    
    # Insertar en la colección mock
    users_collection = mock_db.get_collection('users')
    users_collection.insert_one(user_data)
    
    return user_data

@pytest.fixture
def user_token(app, test_user):
    """Fixture que genera un token JWT válido usando Flask-JWT-Extended"""
    with app.app_context():
        # Usar create_access_token de Flask-JWT-Extended
        token = create_access_token(
            identity=test_user['_id'],
            additional_claims={
                'email': test_user['email'],
                'rol': test_user['rol']
            }
        )
        return token

@pytest.fixture  
def admin_token(app, mock_db, sample_admin_data):
    """Token para usuario administrador"""
    from werkzeug.security import generate_password_hash
    
    admin_data = sample_admin_data.copy()
    admin_data['password'] = generate_password_hash(admin_data['password'])
    admin_data['_id'] = '507f1f77bcf86cd799439012'
    
    # Insertar admin en la colección mock
    users_collection = mock_db.get_collection('users')
    users_collection.insert_one(admin_data)
    
    with app.app_context():
        token = create_access_token(
            identity=admin_data['_id'],
            additional_claims={
                'email': admin_data['email'],
                'rol': admin_data['rol']
            }
        )
        return token

@pytest.fixture
def auth_headers(user_token):
    """Headers con token de autorización"""
    return {'Authorization': f'Bearer {user_token}'}

@pytest.fixture
def admin_headers(admin_token):
    """Headers con token de administrador"""
    return {'Authorization': f'Bearer {admin_token}'}