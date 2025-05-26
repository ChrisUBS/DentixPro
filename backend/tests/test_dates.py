# test_dates.py - Pruebas unitarias para endpoints de citas
import pytest
import json
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from unittest.mock import patch, MagicMock
from http import HTTPStatus

class TestDatesEndpoints:
    """Pruebas para endpoints de usuario de citas"""
    
    # def test_create_date_success(self, client, auth_headers, mock_db):
    #     """Test crear cita exitosamente"""
    #     # Configurar mock para que no encuentre citas existentes
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = None
    #     dates_collection.insert_one.return_value = MagicMock(inserted_id=ObjectId())
        
    #     # Datos de cita válidos (fecha futura)
    #     future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    #     date_data = {
    #         "title": "Cita médica",
    #         "date": future_date,
    #         "time": "14:30",
    #         "description": "Consulta general con el doctor"
    #     }
        
    #     response = client.post('/dates', 
    #                          data=json.dumps(date_data),
    #                          content_type='application/json',
    #                          headers=auth_headers)
        
    #     assert response.status_code == HTTPStatus.CREATED
    #     data = json.loads(response.data)
    #     assert data['msg'] == "Cita creada exitosamente"
    #     assert 'date' in data
    #     dates_collection.insert_one.assert_called_once()
    
    # def test_create_date_missing_title(self, client, auth_headers):
    #     """Test crear cita sin título"""
    #     future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    #     date_data = {
    #         "date": future_date,
    #         "time": "14:30",
    #         "description": "Descripción de la cita"
    #     }
        
    #     response = client.post('/dates',
    #                          data=json.dumps(date_data),
    #                          content_type='application/json',
    #                          headers=auth_headers)
        
    #     assert response.status_code == HTTPStatus.BAD_REQUEST
    
    def test_create_date_short_title(self, client, auth_headers):
        """Test crear cita con título muy corto"""
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        date_data = {
            "title": "ABC",  # Menos de 5 caracteres
            "date": future_date,
            "time": "14:30",
            "description": "Descripción de la cita"
        }
        
        response = client.post('/dates',
                             data=json.dumps(date_data),
                             content_type='application/json',
                             headers=auth_headers)
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.data)
        assert "título debe tener al menos 5 caracteres" in data['msg']
    
    def test_create_date_invalid_date_format(self, client, auth_headers):
        """Test crear cita con formato de fecha inválido"""
        date_data = {
            "title": "Cita médica",
            "date": "2024/12/25",  # Formato incorrecto
            "time": "14:30",
            "description": "Descripción de la cita"
        }
        
        response = client.post('/dates',
                             data=json.dumps(date_data),
                             content_type='application/json',
                             headers=auth_headers)
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.data)
        assert "Formato de fecha inválido" in data['msg']
    
    def test_create_date_invalid_time_format(self, client, auth_headers):
        """Test crear cita con formato de hora inválido"""
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        date_data = {
            "title": "Cita médica",
            "date": future_date,
            "time": "2:30 PM",  # Formato incorrecto
            "description": "Descripción de la cita"
        }
        
        response = client.post('/dates',
                             data=json.dumps(date_data),
                             content_type='application/json',
                             headers=auth_headers)
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.data)
        assert "Formato de hora inválido" in data['msg']
    
    def test_create_date_past_date(self, client, auth_headers):
        """Test crear cita con fecha pasada"""
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        date_data = {
            "title": "Cita médica",
            "date": past_date,
            "time": "14:30",
            "description": "Descripción de la cita"
        }
        
        response = client.post('/dates',
                             data=json.dumps(date_data),
                             content_type='application/json',
                             headers=auth_headers)
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.data)
        assert "debe ser en el futuro" in data['msg']
    
    # def test_create_date_time_conflict(self, client, auth_headers, mock_db):
    #     """Test crear cita en horario ya ocupado"""
    #     # Configurar mock para simular cita existente
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = {"_id": ObjectId(), "status": "pending"}
        
    #     future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    #     date_data = {
    #         "title": "Cita médica",
    #         "date": future_date,
    #         "time": "14:30",
    #         "description": "Descripción de la cita"
    #     }
        
    #     response = client.post('/dates',
    #                          data=json.dumps(date_data),
    #                          content_type='application/json',
    #                          headers=auth_headers)
        
    #     assert response.status_code == HTTPStatus.CONFLICT
    #     data = json.loads(response.data)
    #     assert "horario ya está ocupado" in data['msg']
    
    def test_create_date_no_auth(self, client):
        """Test crear cita sin autenticación"""
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        date_data = {
            "title": "Cita médica",
            "date": future_date,
            "time": "14:30",
            "description": "Descripción de la cita"
        }
        
        response = client.post('/dates',
                             data=json.dumps(date_data),
                             content_type='application/json')
        
        assert response.status_code == HTTPStatus.UNAUTHORIZED
    
    # def test_cancel_date_success(self, client, auth_headers, mock_db):
    #     """Test cancelar cita exitosamente"""
    #     date_id = str(ObjectId())
        
    #     # Configurar mocks
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = {
    #         "_id": ObjectId(date_id),
    #         "userId": "507f1f77bcf86cd799439011",  # Same as test_user fixture
    #         "status": "pending"
    #     }
    #     dates_collection.update_one.return_value = MagicMock(modified_count=1)
        
    #     response = client.delete(f'/dates/{date_id}', headers=auth_headers)
        
    #     assert response.status_code == HTTPStatus.OK
    #     data = json.loads(response.data)
    #     assert data['msg'] == "Cita cancelada exitosamente"
    #     dates_collection.update_one.assert_called_once()
    
    # def test_cancel_date_not_found(self, client, auth_headers, mock_db):
    #     """Test cancelar cita que no existe"""
    #     date_id = str(ObjectId())
        
    #     # Configurar mock para que no encuentre la cita
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = None
        
    #     response = client.delete(f'/dates/{date_id}', headers=auth_headers)
        
    #     assert response.status_code == HTTPStatus.NOT_FOUND
    #     data = json.loads(response.data)
    #     assert "no encontrada" in data['msg']
    
    # def test_cancel_date_not_owner(self, client, auth_headers, mock_db):
    #     """Test cancelar cita de otro usuario (sin ser admin)"""
    #     date_id = str(ObjectId())
        
    #     # Configurar mocks
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = {
    #         "_id": ObjectId(date_id),
    #         "userId": "different_user_id",  # Diferente al usuario de prueba
    #         "status": "pending"
    #     }
        
    #     users_collection = mock_db.get_collection('users')
    #     users_collection.find_one.return_value = {
    #         "userId": "507f1f77bcf86cd799439011",
    #         "rol": "user"  # No es admin
    #     }
        
    #     response = client.delete(f'/dates/{date_id}', headers=auth_headers)
        
    #     assert response.status_code == HTTPStatus.FORBIDDEN
    #     data = json.loads(response.data)
    #     assert "No tiene permiso" in data['msg']
    
    # def test_cancel_date_already_cancelled(self, client, auth_headers, mock_db):
    #     """Test cancelar cita ya cancelada"""
    #     date_id = str(ObjectId())
        
    #     # Configurar mock
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = {
    #         "_id": ObjectId(date_id),
    #         "userId": "507f1f77bcf86cd799439011",
    #         "status": "cancelled"  # Ya cancelada
    #     }
        
    #     response = client.delete(f'/dates/{date_id}', headers=auth_headers)
        
    #     assert response.status_code == HTTPStatus.BAD_REQUEST
    #     data = json.loads(response.data)
    #     assert "No se puede cancelar" in data['msg']
    
    # def test_cancel_date_invalid_id(self, client, auth_headers):
    #     """Test cancelar cita con ID inválido"""
    #     response = client.delete('/dates/invalid_id', headers=auth_headers)
        
    #     assert response.status_code == HTTPStatus.BAD_REQUEST
    #     data = json.loads(response.data)
    #     assert "ID de cita inválido" in data['msg']

class TestAdminDatesEndpoints:
    """Pruebas para endpoints de administrador de citas"""
    
    # def test_get_all_dates_success(self, client, admin_headers):
    #     """Test obtener todas las citas como admin"""
    #     with patch('routes.dates.paginate_results') as mock_paginate:
    #         mock_paginate.return_value = {
    #             'data': [],
    #             'pagination': {
    #                 'page': 1,
    #                 'page_size': 10,
    #                 'total': 0,
    #                 'pages': 0
    #             }
    #         }
            
    #         response = client.get('/admin/dates', headers=admin_headers)
            
    #         assert response.status_code == HTTPStatus.OK
    #         mock_paginate.assert_called_once()
    
    # def test_get_all_dates_with_filters(self, client, admin_headers):
    #     """Test obtener citas con filtros"""
    #     with patch('routes.dates.paginate_results') as mock_paginate:
    #         mock_paginate.return_value = {'data': [], 'pagination': {}}
            
    #         response = client.get('/admin/dates?status=pending&page=2&page_size=5', 
    #                             headers=admin_headers)
            
    #         assert response.status_code == HTTPStatus.OK
    #         # Verificar que se llamó con los parámetros correctos
    #         call_args = mock_paginate.call_args
    #         assert call_args[1]['page'] == 2
    #         assert call_args[1]['page_size'] == 5
    
    def test_get_all_dates_no_admin(self, client, auth_headers):
        """Test obtener todas las citas sin permisos de admin"""
        response = client.get('/admin/dates', headers=auth_headers)
        
        assert response.status_code == HTTPStatus.FORBIDDEN
    
    # def test_update_date_success(self, client, admin_headers, mock_db):
    #     """Test actualizar cita como admin"""
    #     date_id = str(ObjectId())
        
    #     # Configurar mock
    #     with patch('routes.dates.date_exists', return_value=True):
    #         dates_collection = mock_db.get_collection('dates')
    #         dates_collection.update_one.return_value = MagicMock(modified_count=1)
            
    #         update_data = {
    #             "title": "Cita actualizada",
    #             "description": "Nueva descripción actualizada"
    #         }
            
    #         response = client.put(f'/admin/dates/{date_id}',
    #                             data=json.dumps(update_data),
    #                             content_type='application/json',
    #                             headers=admin_headers)
            
    #         assert response.status_code == HTTPStatus.OK
    #         data = json.loads(response.data)
    #         assert data['msg'] == "Cita actualizada exitosamente"
    
    # def test_update_date_not_found(self, client, admin_headers):
    #     """Test actualizar cita que no existe"""
    #     date_id = str(ObjectId())
        
    #     with patch('routes.dates.date_exists', return_value=False):
    #         update_data = {"title": "Cita actualizada"}
            
    #         response = client.put(f'/admin/dates/{date_id}',
    #                             data=json.dumps(update_data),
    #                             content_type='application/json',
    #                             headers=admin_headers)
            
    #         assert response.status_code == HTTPStatus.NOT_FOUND
    
    # def test_update_date_invalid_title(self, client, admin_headers):
    #     """Test actualizar cita con título inválido"""
    #     date_id = str(ObjectId())
        
    #     update_data = {"title": "ABC"}  # Título muy corto
        
    #     response = client.put(f'/admin/dates/{date_id}',
    #                         data=json.dumps(update_data),
    #                         content_type='application/json',
    #                         headers=admin_headers)
        
    #     assert response.status_code == HTTPStatus.BAD_REQUEST
    #     data = json.loads(response.data)
    #     assert "título debe tener al menos 5 caracteres" in data['msg']
    
    # def test_update_date_invalid_status(self, client, admin_headers):
    #     """Test actualizar cita con estado inválido"""
    #     date_id = str(ObjectId())
        
    #     with patch('routes.dates.date_exists', return_value=True):
    #         update_data = {"status": "invalid_status"}
            
    #         response = client.put(f'/admin/dates/{date_id}',
    #                             data=json.dumps(update_data),
    #                             content_type='application/json',
    #                             headers=admin_headers)
            
    #         assert response.status_code == HTTPStatus.BAD_REQUEST
    #         data = json.loads(response.data)
    #         assert "Estado inválido" in data['msg']
    
    # def test_complete_date_success(self, client, admin_headers, mock_db):
    #     """Test marcar cita como completada"""
    #     date_id = str(ObjectId())
        
    #     # Configurar mocks
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = {
    #         "_id": ObjectId(date_id),
    #         "status": "pending"
    #     }
    #     dates_collection.update_one.return_value = MagicMock(modified_count=1)
        
    #     response = client.put(f'/admin/dates/{date_id}/complete', 
    #                         headers=admin_headers)
        
    #     assert response.status_code == HTTPStatus.OK
    #     data = json.loads(response.data)
    #     assert "completada exitosamente" in data['msg']
    
    # def test_complete_date_not_found(self, client, admin_headers, mock_db):
    #     """Test completar cita que no existe"""
    #     date_id = str(ObjectId())
        
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = None
        
    #     response = client.put(f'/admin/dates/${date_id}/complete', 
    #                         headers=admin_headers)
        
    #     assert response.status_code == HTTPStatus.NOT_FOUND
    
    # def test_complete_date_already_completed(self, client, admin_headers, mock_db):
    #     """Test completar cita ya completada"""
    #     date_id = str(ObjectId())
        
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = {
    #         "_id": ObjectId(date_id),
    #         "status": "completed"
    #     }
        
    #     response = client.put(f'/admin/dates/{date_id}/complete', 
    #                         headers=admin_headers)
        
    #     assert response.status_code == HTTPStatus.BAD_REQUEST
    #     data = json.loads(response.data)
    #     assert "No se puede completar" in data['msg']
    
    # def test_admin_cancel_date_success(self, client, admin_headers, mock_db):
    #     """Test cancelar cita como admin"""
    #     date_id = str(ObjectId())
        
    #     # Configurar mocks
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = {
    #         "_id": ObjectId(date_id),
    #         "status": "pending"
    #     }
    #     dates_collection.update_one.return_value = MagicMock(modified_count=1)
        
    #     response = client.put(f'/admin/dates/{date_id}/cancel', 
    #                         headers=admin_headers)
        
    #     assert response.status_code == HTTPStatus.OK
    #     data = json.loads(response.data)
    #     assert "cancelada exitosamente" in data['msg']
    
    # def test_admin_cancel_date_not_found(self, client, admin_headers, mock_db):
    #     """Test cancelar cita que no existe (admin)"""
    #     date_id = str(ObjectId())
        
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.find_one.return_value = None
        
    #     response = client.put(f'/admin/dates/{date_id}/cancel', 
    #                         headers=admin_headers)
        
    #     assert response.status_code == HTTPStatus.NOT_FOUND
    
    def test_admin_endpoints_no_auth(self, client):
        """Test endpoints de admin sin autenticación"""
        date_id = str(ObjectId())
        
        # Test todos los endpoints de admin
        endpoints = [
            ('GET', '/admin/dates'),
            ('PUT', f'/admin/dates/{date_id}'),
            ('PUT', f'/admin/dates/{date_id}/complete'),
            ('PUT', f'/admin/dates/{date_id}/cancel')
        ]
        
        for method, endpoint in endpoints:
            if method == 'GET':
                response = client.get(endpoint)
            elif method == 'PUT':
                response = client.put(endpoint, 
                                    data=json.dumps({}),
                                    content_type='application/json')
            
            assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestHelperFunctions:
    """Pruebas para funciones auxiliares"""
    
    def test_validate_date_format_valid(self):
        """Test validación de formato de fecha válido"""
        from routes.dates import validate_date_format
        
        assert validate_date_format("2024-12-25") == True
        assert validate_date_format("2024-01-01") == True
    
    def test_validate_date_format_invalid(self):
        """Test validación de formato de fecha inválido"""
        from routes.dates import validate_date_format
        
        assert validate_date_format("2024/12/25") == False
        assert validate_date_format("25-12-2024") == False
        assert validate_date_format("invalid") == False
    
    def test_validate_time_format_valid(self):
        """Test validación de formato de hora válido"""
        from routes.dates import validate_time_format
        
        assert validate_time_format("14:30") == True
        assert validate_time_format("00:00") == True
        assert validate_time_format("23:59") == True
    
    def test_validate_time_format_invalid(self):
        """Test validación de formato de hora inválido"""
        from routes.dates import validate_time_format
        
        assert validate_time_format("2:30 PM") == False
        assert validate_time_format("24:00") == False
        assert validate_time_format("14:60") == False
        assert validate_time_format("invalid") == False
    
    # def test_date_exists(self, mock_db):
    #     """Test función date_exists"""
    #     from routes.dates import date_exists
        
    #     date_id = str(ObjectId())
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.count_documents.return_value = 1
        
    #     result = date_exists(date_id)
    #     assert result == True
        
    #     dates_collection.count_documents.return_value = 0
    #     result = date_exists(date_id)
    #     assert result == False
    
    # def test_is_date_owner(self, mock_db):
    #     """Test función is_date_owner"""
    #     from routes.dates import is_date_owner
        
    #     date_id = str(ObjectId())
    #     user_id = "test_user_id"
        
    #     dates_collection = mock_db.get_collection('dates')
    #     dates_collection.count_documents.return_value = 1
        
    #     result = is_date_owner(date_id, user_id)
    #     assert result == True
        
    #     dates_collection.count_documents.return_value = 0
    #     result = is_date_owner(date_id, user_id)
    #     assert result == False