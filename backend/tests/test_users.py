# test_users.py - Pruebas unitarias para endpoints de usuarios
import pytest
import json
from http import HTTPStatus
from unittest.mock import patch
from werkzeug.security import generate_password_hash, check_password_hash

class TestUserEndpoints:
    """Pruebas para endpoints de usuario regular"""
    
    # def test_get_current_user_success(self, client, user_token):
    #     """Test para obtener información del usuario actual - éxito"""
    #     headers = {'Authorization': f'Bearer {user_token}'}
    #     response = client.get('/users/me', headers=headers)
        
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert 'name' in data
    #     assert 'email' in data
    #     assert 'rol' in data
    #     assert 'password' not in data
    
    def test_get_current_user_no_token(self, client):
        """Test para obtener usuario actual sin token - error"""
        response = client.get('/users/me')
        assert response.status_code == 401
    
    # def test_get_current_user_not_found(self, client, app):
    #     """Test para obtener usuario que no existe"""
    #     with app.application_context():
    #         from flask_jwt_extended import create_access_token
    #         token = create_access_token(identity="nonexistent_user")
        
    #     headers = {'Authorization': f'Bearer {token}'}
    #     response = client.get('/users/me', headers=headers)
        
    #     assert response.status_code == 404
    #     data = json.loads(response.data)
    #     assert data['msg'] == "Usuario no encontrado"
    
    def test_update_current_user_success(self, client, user_token):
        """Test para actualizar información del usuario actual - éxito"""
        headers = {'Authorization': f'Bearer {user_token}'}
        update_data = {
            'name': 'Updated Test User',
            'email': 'updated@example.com'
        }
        
        response = client.put('/users/me', 
                            data=json.dumps(update_data), 
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['msg'] == "Información actualizada exitosamente"
        assert 'user' in data
    
    def test_update_current_user_no_data(self, client, user_token):
        """Test para actualizar usuario sin datos"""
        headers = {'Authorization': f'Bearer {user_token}'}
        
        response = client.put('/users/me', 
                            data=json.dumps({}), 
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "No se proporcionaron datos" in data['msg']
    
    def test_update_current_user_forbidden_fields(self, client, user_token):
        """Test para actualizar campos prohibidos"""
        headers = {'Authorization': f'Bearer {user_token}'}
        update_data = {
            'userId': 'hacker_attempt',
            'password': 'hacked_password',
            'rol': 'admin',
            'name': 'Valid Name'
        }
        
        response = client.put('/users/me', 
                            data=json.dumps(update_data), 
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 200  # Solo debe actualizar campos válidos
        data = json.loads(response.data)
        assert data['msg'] == "Información actualizada exitosamente"
    
    def test_update_current_user_invalid_name(self, client, user_token):
        """Test para actualizar con nombre inválido"""
        headers = {'Authorization': f'Bearer {user_token}'}
        update_data = {'name': 'ab'}  # Muy corto
        
        response = client.put('/users/me', 
                            data=json.dumps(update_data), 
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "al menos 3 caracteres" in data['msg']
    
    # def test_change_password_success(self, client, user_token, mock_db):
    #     """Test para cambiar contraseña - éxito"""
    #     headers = {'Authorization': f'Bearer {user_token}'}
    #     password_data = {
    #         'current_password': 'testpassword123',
    #         'new_password': 'newpassword123'
    #     }
        
    #     response = client.put('/users/me/password', 
    #                         data=json.dumps(password_data), 
    #                         content_type='application/json',
    #                         headers=headers)
        
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert data['msg'] == "Contraseña actualizada exitosamente"
    
    def test_change_password_missing_fields(self, client, user_token):
        """Test para cambiar contraseña sin campos requeridos"""
        headers = {'Authorization': f'Bearer {user_token}'}
        password_data = {'current_password': 'testpassword123'}  # Falta new_password
        
        response = client.put('/users/me/password', 
                            data=json.dumps(password_data), 
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 400
    
    def test_change_password_invalid_new_password(self, client, user_token):
        """Test para cambiar contraseña con nueva contraseña inválida"""
        headers = {'Authorization': f'Bearer {user_token}'}
        password_data = {
            'current_password': 'testpassword123',
            'new_password': '123'  # Muy corta
        }
        
        response = client.put('/users/me/password', 
                            data=json.dumps(password_data), 
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "al menos 8 caracteres" in data['msg']
    
    # def test_change_password_wrong_current_password(self, client, user_token):
    #     """Test para cambiar contraseña con contraseña actual incorrecta"""
    #     headers = {'Authorization': f'Bearer {user_token}'}
    #     password_data = {
    #         'current_password': 'wrongpassword',
    #         'new_password': 'newpassword123'
    #     }
        
    #     response = client.put('/users/me/password', 
    #                         data=json.dumps(password_data), 
    #                         content_type='application/json',
    #                         headers=headers)
        
    #     assert response.status_code == 401
    #     data = json.loads(response.data)
    #     assert "Contraseña actual incorrecta" in data['msg']
    
    # def test_get_user_dates_success(self, client, user_token, mock_db):
    #     """Test para obtener citas del usuario"""
    #     # Crear algunas citas mock
    #     dates_collection = mock_db.get_collection("dates")
    #     sample_dates = [
    #         {"userId": "test_user_123", "date": "2024-12-01T10:00:00", "status": "programada"},
    #         {"userId": "test_user_123", "date": "2024-12-02T14:00:00", "status": "completada"},
    #     ]
    #     dates_collection.insert_many(sample_dates)
        
    #     headers = {'Authorization': f'Bearer {user_token}'}
    #     response = client.get('/users/me/dates', headers=headers)
        
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert 'data' in data
    #     assert 'total' in data
    #     assert 'page' in data
    #     assert 'page_size' in data
    
    def test_get_user_dates_with_filters(self, client, user_token, mock_db):
        """Test para obtener citas del usuario con filtros"""
        # Crear algunas citas mock
        dates_collection = mock_db.get_collection("dates")
        sample_dates = [
            {"userId": "test_user_123", "date": "2024-12-01T10:00:00", "status": "programada"},
            {"userId": "test_user_123", "date": "2024-12-02T14:00:00", "status": "completada"},
        ]
        dates_collection.insert_many(sample_dates)
        
        headers = {'Authorization': f'Bearer {user_token}'}
        response = client.get('/users/me/dates?status=programada&page=1&page_size=5', 
                            headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data


class TestAdminUserEndpoints:
    """Pruebas para endpoints administrativos de usuarios"""
    
    # def test_get_all_users_success(self, client, admin_token, mock_db):
    #     """Test para obtener todos los usuarios (admin)"""
    #     # Crear algunos usuarios mock
    #     users_collection = mock_db.get_collection("users")
    #     sample_users = [
    #         {"userId": "user1", "name": "User 1", "email": "user1@test.com", "rol": "user", "password": "hashed"},
    #         {"userId": "user2", "name": "User 2", "email": "user2@test.com", "rol": "user", "password": "hashed"},
    #     ]
    #     users_collection.insert_many(sample_users)
        
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     response = client.get('/users', headers=headers)
        
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert 'data' in data
    #     assert 'total' in data
    #     # Verificar que no se incluyan contraseñas
    #     for user in data['data']:
    #         assert 'password' not in user
    
    def test_get_all_users_not_admin(self, client, user_token):
        """Test para obtener todos los usuarios sin ser admin"""
        headers = {'Authorization': f'Bearer {user_token}'}
        response = client.get('/users', headers=headers)
        
        assert response.status_code == 403
    
    # def test_get_all_users_with_role_filter(self, client, admin_token, mock_db):
    #     """Test para obtener usuarios filtrado por rol"""
    #     # Crear usuarios mock con diferentes roles
    #     users_collection = mock_db.get_collection("users")
    #     sample_users = [
    #         {"userId": "user1", "name": "User 1", "rol": "user", "password": "hashed"},
    #         {"userId": "admin1", "name": "Admin 1", "rol": "admin", "password": "hashed"},
    #     ]
    #     users_collection.insert_many(sample_users)
        
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     response = client.get('/users?rol=admin', headers=headers)
        
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert 'data' in data
    
    # def test_get_user_by_id_success(self, client, admin_token, mock_db):
    #     """Test para obtener usuario por ID (admin)"""
    #     # Crear usuario mock
    #     users_collection = mock_db.get_collection("users")
    #     user_data = {
    #         "userId": "target_user",
    #         "name": "Target User",
    #         "email": "target@test.com",
    #         "rol": "user",
    #         "password": "hashed"
    #     }
    #     users_collection.insert_one(user_data)
        
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     response = client.get('/users/target_user', headers=headers)
        
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert data['name'] == "Target User"
    #     assert 'password' not in data  # No debe incluir contraseña
    
    # def test_get_user_by_id_not_found(self, client, admin_token):
    #     """Test para obtener usuario que no existe"""
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     response = client.get('/users/nonexistent_user', headers=headers)
        
    #     assert response.status_code == 404
    #     data = json.loads(response.data)
    #     assert data['msg'] == "Usuario no encontrado"
    
    def test_get_user_by_id_not_admin(self, client, user_token):
        """Test para obtener usuario por ID sin ser admin"""
        headers = {'Authorization': f'Bearer {user_token}'}
        response = client.get('/users/some_user', headers=headers)
        
        assert response.status_code == 403
    
    # def test_update_user_success(self, client, admin_token, mock_db):
    #     """Test para actualizar usuario (admin)"""
    #     # Crear usuario mock
    #     users_collection = mock_db.get_collection("users")
    #     user_data = {
    #         "userId": "target_user",
    #         "name": "Target User",
    #         "email": "target@test.com",
    #         "rol": "user"
    #     }
    #     users_collection.insert_one(user_data)
        
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     update_data = {
    #         'name': 'Updated User Name',
    #         'rol': 'admin'
    #     }
        
    #     response = client.put('/users/target_user',
    #                         data=json.dumps(update_data),
    #                         content_type='application/json',
    #                         headers=headers)
        
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert data['msg'] == "Usuario actualizado exitosamente"
    
    # def test_update_user_invalid_role(self, client, admin_token, mock_db):
    #     """Test para actualizar usuario con rol inválido"""
    #     # Crear usuario mock
    #     users_collection = mock_db.get_collection("users")
    #     user_data = {"userId": "target_user", "name": "Target User", "rol": "user"}
    #     users_collection.insert_one(user_data)
        
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     update_data = {'rol': 'invalid_role'}
        
    #     response = client.put('/users/target_user',
    #                         data=json.dumps(update_data),
    #                         content_type='application/json',
    #                         headers=headers)
        
    #     assert response.status_code == 400
    #     data = json.loads(response.data)
    #     assert "Rol inválido" in data['msg']
    
    # def test_update_user_not_found(self, client, admin_token):
    #     """Test para actualizar usuario que no existe"""
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     update_data = {'name': 'New Name'}
        
    #     response = client.put('/users/nonexistent_user',
    #                         data=json.dumps(update_data),
    #                         content_type='application/json',
    #                         headers=headers)
        
    #     assert response.status_code == 404
    #     data = json.loads(response.data)
    #     assert data['msg'] == "Usuario no encontrado"
    
    def test_update_user_not_admin(self, client, user_token):
        """Test para actualizar usuario sin ser admin"""
        headers = {'Authorization': f'Bearer {user_token}'}
        update_data = {'name': 'Hacker Name'}
        
        response = client.put('/users/some_user',
                            data=json.dumps(update_data),
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 403
    
    # def test_reset_user_password_success(self, client, admin_token, mock_db):
    #     """Test para resetear contraseña de usuario (admin)"""
    #     # Crear usuario mock
    #     users_collection = mock_db.get_collection("users")
    #     user_data = {
    #         "userId": "target_user",
    #         "name": "Target User",
    #         "password": "old_hashed_password"
    #     }
    #     users_collection.insert_one(user_data)
        
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     password_data = {'new_password': 'newpassword123'}
        
    #     response = client.put('/users/target_user/reset-password',
    #                         data=json.dumps(password_data),
    #                         content_type='application/json',
    #                         headers=headers)
        
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert data['msg'] == "Contraseña reseteada exitosamente"
    
    # def test_reset_user_password_invalid_password(self, client, admin_token, mock_db):
    #     """Test para resetear contraseña con contraseña inválida"""
    #     # Crear usuario mock
    #     users_collection = mock_db.get_collection("users")
    #     user_data = {"userId": "target_user", "name": "Target User"}
    #     users_collection.insert_one(user_data)
        
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     password_data = {'new_password': '123'}  # Muy corta
        
    #     response = client.put('/users/target_user/reset-password',
    #                         data=json.dumps(password_data),
    #                         content_type='application/json',
    #                         headers=headers)
        
    #     assert response.status_code == 400
    #     data = json.loads(response.data)
    #     assert "al menos 8 caracteres" in data['msg']
    
    # def test_reset_user_password_missing_field(self, client, admin_token):
    #     """Test para resetear contraseña sin campo requerido"""
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     password_data = {}  # Falta new_password
        
    #     response = client.put('/users/target_user/reset-password',
    #                         data=json.dumps(password_data),
    #                         content_type='application/json',
    #                         headers=headers)
        
    #     assert response.status_code == 400
    
    # def test_reset_user_password_user_not_found(self, client, admin_token):
    #     """Test para resetear contraseña de usuario que no existe"""
    #     headers = {'Authorization': f'Bearer {admin_token}'}
    #     password_data = {'new_password': 'newpassword123'}
        
    #     response = client.put('/users/nonexistent_user/reset-password',
    #                         data=json.dumps(password_data),
    #                         content_type='application/json',
    #                         headers=headers)
        
    #     assert response.status_code == 404
    #     data = json.loads(response.data)
    #     assert data['msg'] == "Usuario no encontrado"
    
    def test_reset_user_password_not_admin(self, client, user_token):
        """Test para resetear contraseña sin ser admin"""
        headers = {'Authorization': f'Bearer {user_token}'}
        password_data = {'new_password': 'newpassword123'}
        
        response = client.put('/users/some_user/reset-password',
                            data=json.dumps(password_data),
                            content_type='application/json',
                            headers=headers)
        
        assert response.status_code == 403


class TestUserEndpointsIntegration:
    """Pruebas de integración para endpoints de usuarios"""
    
    # @patch('utils.get_user_data')
    # def test_get_current_user_with_mock_utils(self, mock_get_user_data, client, user_token):
    #     """Test para verificar integración con función get_user_data"""
    #     # Configurar mock
    #     mock_get_user_data.return_value = {
    #         "userId": "test_user_123",
    #         "name": "Test User",
    #         "email": "test@example.com",
    #         "rol": "user"
    #     }
        
    #     headers = {'Authorization': f'Bearer {user_token}'}
    #     response = client.get('/users/me', headers=headers)
        
    #     assert response.status_code == 200
    #     mock_get_user_data.assert_called_once_with("test_user_123")
    
    # @patch('utils.paginate_results')
    # def test_get_user_dates_with_mock_paginate(self, mock_paginate, client, user_token):
    #     """Test para verificar integración con función paginate_results"""
    #     # Configurar mock
    #     mock_paginate.return_value = {
    #         "data": [],
    #         "total": 0,
    #         "page": 1,
    #         "page_size": 10,
    #         "total_pages": 0
    #     }
        
    #     headers = {'Authorization': f'Bearer {user_token}'}
    #     response = client.get('/users/me/dates', headers=headers)
        
    #     assert response.status_code == 200
    #     mock_paginate.assert_called_once()