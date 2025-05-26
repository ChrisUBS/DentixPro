# tests/test_auth.py - Pruebas unitarias para auth.py
import pytest
import json
from http import HTTPStatus
from werkzeug.security import generate_password_hash
from unittest.mock import patch
from bson.objectid import ObjectId
from datetime import datetime

class TestLogin:
    """Pruebas para el endpoint de login"""
    
    def test_login_success(self, client, mock_db, sample_user_data):
        """Test login exitoso"""
        # Preparar datos en la BD mock
        users_collection = mock_db.get_collection("users")
        user_id = str(ObjectId())
        hashed_password = generate_password_hash(sample_user_data["password"])
        
        user_doc = {
            "userId": user_id,
            "name": sample_user_data["name"],
            "email": sample_user_data["email"],
            "password": hashed_password,
            "rol": sample_user_data["rol"],
            "created_at": datetime.utcnow()
        }
        users_collection.insert_one(user_doc)
        
        # Mock get_user_data
        with patch('routes.auth.get_user_data') as mock_get_user:
            mock_get_user.return_value = {
                "userId": user_id,
                "name": sample_user_data["name"],
                "email": sample_user_data["email"],
                "rol": sample_user_data["rol"]
            }
            
            # Hacer request
            response = client.post('/auth/login', 
                json={
                    "email": sample_user_data["email"],
                    "password": sample_user_data["password"]
                },
                content_type='application/json'
            )
            
            # Verificar respuesta
            assert response.status_code == HTTPStatus.OK
            data = json.loads(response.data)
            assert "access_token" in data
            assert "user" in data
            assert data["user"]["email"] == sample_user_data["email"]
    
    def test_login_invalid_credentials_wrong_password(self, client, mock_db, sample_user_data):
        """Test login con contraseña incorrecta"""
        # Preparar datos en la BD mock
        users_collection = mock_db.get_collection("users")
        user_id = str(ObjectId())
        hashed_password = generate_password_hash(sample_user_data["password"])
        
        user_doc = {
            "userId": user_id,
            "email": sample_user_data["email"],
            "password": hashed_password
        }
        users_collection.insert_one(user_doc)
        
        # Hacer request con contraseña incorrecta
        response = client.post('/auth/login', 
            json={
                "email": sample_user_data["email"],
                "password": "wrongpassword"
            },
            content_type='application/json'
        )
        
        # Verificar respuesta
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        data = json.loads(response.data)
        assert data["msg"] == "Credenciales inválidas"
    
    def test_login_user_not_found(self, client, mock_db):
        """Test login con usuario inexistente"""
        response = client.post('/auth/login', 
            json={
                "email": "nonexistent@example.com",
                "password": "somepassword"
            },
            content_type='application/json'
        )
        
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        data = json.loads(response.data)
        assert data["msg"] == "Credenciales inválidas"
    
    def test_login_missing_fields(self, client):
        """Test login sin campos requeridos"""
        # Sin email
        response = client.post('/auth/login', 
            json={"password": "testpass"},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        
        # Sin password
        response = client.post('/auth/login', 
            json={"email": "test@example.com"},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
    
    def test_login_empty_fields(self, client):
        """Test login con campos vacíos"""
        response = client.post('/auth/login', 
            json={
                "email": "",
                "password": ""
            },
            content_type='application/json'
        )
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.data)
        assert data["msg"] == "Email y contraseña son requeridos"


class TestSignup:
    """Pruebas para el endpoint de signup"""
    
    def test_signup_success(self, client, mock_db, sample_user_data):
        """Test registro exitoso"""
        with patch('routes.auth.get_user_data') as mock_get_user:
            mock_get_user.return_value = {
                "userId": "test_user_id",
                "name": sample_user_data["name"],
                "email": sample_user_data["email"],
                "rol": sample_user_data["rol"]
            }
            
            response = client.post('/auth/signup', 
                json=sample_user_data,
                content_type='application/json'
            )
            
            assert response.status_code == HTTPStatus.CREATED
            data = json.loads(response.data)
            assert data["msg"] == "Usuario creado exitosamente"
            assert "access_token" in data
            assert "user" in data
            
            # Verificar que el usuario se guardó en la BD
            users_collection = mock_db.get_collection("users")
            saved_user = users_collection.find_one({"email": sample_user_data["email"]})
            assert saved_user is not None
            assert saved_user["name"] == sample_user_data["name"]
            assert saved_user["rol"] == sample_user_data["rol"]
    
    def test_signup_duplicate_email(self, client, mock_db, sample_user_data):
        """Test registro con email duplicado"""
        # Insertar usuario existente
        users_collection = mock_db.get_collection("users")
        existing_user = {
            "userId": str(ObjectId()),
            "email": sample_user_data["email"],
            "name": "Existing User",
            "password": "hashedpass",
            "rol": "user"
        }
        users_collection.insert_one(existing_user)
        
        # Intentar registrar con mismo email
        response = client.post('/auth/signup', 
            json=sample_user_data,
            content_type='application/json'
        )
        
        assert response.status_code == HTTPStatus.CONFLICT
        data = json.loads(response.data)
        assert data["msg"] == "Ya existe un usuario con este email"
    
    def test_signup_invalid_name(self, client, sample_user_data):
        """Test registro con nombre inválido"""
        invalid_data = sample_user_data.copy()
        invalid_data["name"] = "ab"  # Menos de 3 caracteres
        
        response = client.post('/auth/signup', 
            json=invalid_data,
            content_type='application/json'
        )
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.data)
        assert data["msg"] == "El nombre debe tener al menos 3 caracteres"
    
    def test_signup_invalid_email(self, client, sample_user_data):
        """Test registro con email inválido"""
        invalid_data = sample_user_data.copy()
        invalid_data["email"] = "invalid-email"
        
        response = client.post('/auth/signup', 
            json=invalid_data,
            content_type='application/json'
        )
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.data)
        assert data["msg"] == "Email inválido"
    
    def test_signup_weak_password(self, client, sample_user_data):
        """Test registro con contraseña débil"""
        invalid_data = sample_user_data.copy()
        invalid_data["password"] = "1234567"  # Menos de 8 caracteres
        
        response = client.post('/auth/signup', 
            json=invalid_data,
            content_type='application/json'
        )
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.data)
        assert data["msg"] == "La contraseña debe tener al menos 8 caracteres"
    
    def test_signup_invalid_role(self, client, sample_user_data):
        """Test registro con rol inválido"""
        invalid_data = sample_user_data.copy()
        invalid_data["rol"] = "invalid_role"
        
        response = client.post('/auth/signup', 
            json=invalid_data,
            content_type='application/json'
        )
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.data)
        assert data["msg"] == "Rol inválido. Debe ser 'admin' o 'user'"
    
    def test_signup_missing_fields(self, client):
        """Test registro sin campos requeridos"""
        response = client.post('/auth/signup', 
            json={"name": "Test User"},
            content_type='application/json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
    
    def test_signup_default_role(self, client, mock_db):
        """Test que el rol por defecto sea 'user'"""
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
            # Sin especificar rol
        }
        
        with patch('routes.auth.get_user_data') as mock_get_user:
            mock_get_user.return_value = {
                "userId": "test_user_id",
                "name": user_data["name"],
                "email": user_data["email"],
                "rol": "user"
            }
            
            response = client.post('/auth/signup', 
                json=user_data,
                content_type='application/json'
            )
            
            assert response.status_code == HTTPStatus.CREATED
            
            # Verificar que el rol por defecto sea 'user'
            users_collection = mock_db.get_collection("users")
            saved_user = users_collection.find_one({"email": user_data["email"]})
            assert saved_user["rol"] == "user"


class TestAuthIntegration:
    """Pruebas de integración para flujos completos"""
    
    def test_signup_then_login(self, client, mock_db, sample_user_data):
        """Test flujo completo: registrarse y luego hacer login"""
        # Registrarse
        with patch('routes.auth.get_user_data') as mock_get_user:
            mock_get_user.return_value = {
                "userId": "test_user_id",
                "name": sample_user_data["name"],
                "email": sample_user_data["email"],
                "rol": sample_user_data["rol"]
            }
            
            signup_response = client.post('/auth/signup', 
                json=sample_user_data,
                content_type='application/json'
            )
            assert signup_response.status_code == HTTPStatus.CREATED
            
            # Login con las mismas credenciales
            login_response = client.post('/auth/login', 
                json={
                    "email": sample_user_data["email"],
                    "password": sample_user_data["password"]
                },
                content_type='application/json'
            )
            
            assert login_response.status_code == HTTPStatus.OK
            login_data = json.loads(login_response.data)
            assert "access_token" in login_data
            assert login_data["user"]["email"] == sample_user_data["email"]