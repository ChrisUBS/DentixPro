# routes/users.py - User routes
from flask import Blueprint, request, jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import logging

from db import Database
from utils import validate_request_json, get_user_data, admin_required, paginate_results

users_bp = Blueprint('users', __name__)
logger = logging.getLogger(__name__)

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    user_id = get_jwt_identity()
    user_data = get_user_data(user_id)
    
    if not user_data:
        return jsonify({"msg": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND
    
    return jsonify(user_data), HTTPStatus.OK

@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current user information"""
    user_id = get_jwt_identity()
    data = request.json
    
    # Check if data is provided
    if not data:
        return jsonify({"msg": "No se proporcionaron datos para actualizar"}), HTTPStatus.BAD_REQUEST
    
    # Prevent updating sensitive fields
    forbidden_fields = ["userId", "password", "rol", "_id"]
    for field in forbidden_fields:
        if field in data:
            data.pop(field)
    
    # Validate name if provided
    if "name" in data and (not data["name"] or len(data["name"].strip()) < 3):
        return jsonify({"msg": "El nombre debe tener al menos 3 caracteres"}), HTTPStatus.BAD_REQUEST
    
    # If empty, return
    if not data:
        return jsonify({"msg": "No se proporcionaron datos válidos para actualizar"}), HTTPStatus.BAD_REQUEST
    
    db_instance = Database.get_instance()
    users_collection = db_instance.get_collection("users")
    
    # Update user
    users_collection.update_one(
        {"userId": user_id},
        {"$set": data}
    )
    
    # Log user update
    logger.info(f"Usuario con ID {user_id} ha actualizado su información")
    
    # Return updated user data
    updated_user = get_user_data(user_id)
    return jsonify({
        "msg": "Información actualizada exitosamente",
        "user": updated_user
    }), HTTPStatus.OK

@users_bp.route('/me/password', methods=['PUT'])
@jwt_required()
@validate_request_json(['current_password', 'new_password'])
def change_password():
    """Change current user password"""
    user_id = get_jwt_identity()
    data = request.json
    
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    
    # Validate new password
    if not new_password or len(new_password) < 8:
        return jsonify({"msg": "La nueva contraseña debe tener al menos 8 caracteres"}), HTTPStatus.BAD_REQUEST
    
    db_instance = Database.get_instance()
    users_collection = db_instance.get_collection("users")
    
    # Get user
    user = users_collection.find_one({"userId": user_id})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND
    
    # Check if current password is correct
    if not check_password_hash(user["password"], current_password):
        return jsonify({"msg": "Contraseña actual incorrecta"}), HTTPStatus.UNAUTHORIZED
    
    # Update password
    hashed_password = generate_password_hash(new_password)
    users_collection.update_one(
        {"userId": user_id},
        {"$set": {"password": hashed_password}}
    )
    
    # Log password change
    logger.info(f"Usuario con ID {user_id} ha cambiado su contraseña")
    
    return jsonify({"msg": "Contraseña actualizada exitosamente"}), HTTPStatus.OK

@users_bp.route('/me/dates', methods=['GET'])
@jwt_required()
def get_user_dates():
    """Get current user appointments"""
    user_id = get_jwt_identity()
    
    # Get query parameters
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    status = request.args.get('status')
    
    # Build query
    query = {"userId": user_id}
    
    # Filter by status if provided
    if status:
        query["status"] = status
    
    # Get paginated results
    result = paginate_results(
        collection="dates", 
        query=query, 
        page=page, 
        page_size=page_size,
        sort_by=("date", 1)  # Sort by date ascending
    )
    
    return jsonify(result), HTTPStatus.OK

# Admin routes for managing users
@users_bp.route('', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users (admin only)"""
    # Get query parameters
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    rol = request.args.get('rol')
    
    # Build query
    query = {}
    
    # Filter by role if provided
    if rol:
        query["rol"] = rol
    
    # Get paginated results
    result = paginate_results(
        collection="users", 
        query=query, 
        page=page, 
        page_size=page_size,
        sort_by=("name", 1)  # Sort by name ascending
    )
    
    # Remove sensitive information
    for user in result["data"]:
        if "password" in user:
            del user["password"]
    
    return jsonify(result), HTTPStatus.OK

@users_bp.route('/<user_id>', methods=['GET'])
@admin_required
def get_user_by_id(user_id):
    """Get user by ID (admin only)"""
    db_instance = Database.get_instance()
    users_collection = db_instance.get_collection("users")
    
    # Find user
    user = users_collection.find_one({"userId": user_id})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND
    
    # Remove sensitive information
    if "password" in user:
        del user["password"]
    
    return jsonify(Database.fix_id(user)), HTTPStatus.OK

@users_bp.route('/<user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user (admin only)"""
    data = request.json
    
    # Check if data is provided
    if not data:
        return jsonify({"msg": "No se proporcionaron datos para actualizar"}), HTTPStatus.BAD_REQUEST
    
    # Prevent updating sensitive fields
    forbidden_fields = ["userId", "password", "_id"]
    for field in forbidden_fields:
        if field in data:
            data.pop(field)
    
    # Validate role if provided
    if "rol" in data and data["rol"] not in ["admin", "user"]:
        return jsonify({"msg": "Rol inválido. Debe ser 'admin' o 'user'"}), HTTPStatus.BAD_REQUEST
    
    # If empty, return
    if not data:
        return jsonify({"msg": "No se proporcionaron datos válidos para actualizar"}), HTTPStatus.BAD_REQUEST
    
    db_instance = Database.get_instance()
    users_collection = db_instance.get_collection("users")
    
    # Check if user exists
    if not users_collection.find_one({"userId": user_id}):
        return jsonify({"msg": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND
    
    # Update user
    users_collection.update_one(
        {"userId": user_id},
        {"$set": data}
    )
    
    # Log user update
    admin_id = get_jwt_identity()
    logger.info(f"Usuario con ID {user_id} actualizado por admin {admin_id}")
    
    # Return updated user data
    updated_user = get_user_data(user_id)
    return jsonify({
        "msg": "Usuario actualizado exitosamente",
        "user": updated_user
    }), HTTPStatus.OK

@users_bp.route('/<user_id>/reset-password', methods=['PUT'])
@admin_required
@validate_request_json(['new_password'])
def reset_user_password(user_id):
    """Reset user password (admin only)"""
    data = request.json
    new_password = data.get("new_password")
    
    # Validate new password
    if not new_password or len(new_password) < 8:
        return jsonify({"msg": "La nueva contraseña debe tener al menos 8 caracteres"}), HTTPStatus.BAD_REQUEST
    
    db_instance = Database.get_instance()
    users_collection = db_instance.get_collection("users")
    
    # Check if user exists
    if not users_collection.find_one({"userId": user_id}):
        return jsonify({"msg": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND
    
    # Update password
    hashed_password = generate_password_hash(new_password)
    users_collection.update_one(
        {"userId": user_id},
        {"$set": {"password": hashed_password}}
    )
    
    # Log password reset
    admin_id = get_jwt_identity()
    logger.info(f"Contraseña de usuario con ID {user_id} reseteada por admin {admin_id}")
    
    return jsonify({"msg": "Contraseña reseteada exitosamente"}), HTTPStatus.OK