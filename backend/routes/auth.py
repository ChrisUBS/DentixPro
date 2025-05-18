# routes/auth.py - Authentication routes
from flask import Blueprint, request, jsonify
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import re
from bson.objectid import ObjectId
import logging
from datetime import datetime

from db import Database
from utils import get_user_data, validate_request_json

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['POST'])
@validate_request_json(['email', 'password'])
def login():
    """Authenticate user and return JWT token"""
    data = request.json
    email = data.get("email").lower().strip()
    password = data.get("password")
    
    # Input validation
    if not email or not password:
        return jsonify({"msg": "Email y contraseña son requeridos"}), HTTPStatus.BAD_REQUEST
    
    db_instance = Database.get_instance()
    users_collection = db_instance.get_collection("users")
    
    # Find user by email
    user = users_collection.find_one({"email": email})
    if not user:
        # Use same error message to prevent user enumeration
        return jsonify({"msg": "Credenciales inválidas"}), HTTPStatus.UNAUTHORIZED
    
    # Verify password
    if not check_password_hash(user.get("password", ""), password):
        return jsonify({"msg": "Credenciales inválidas"}), HTTPStatus.UNAUTHORIZED
    
    # Create access token
    access_token = create_access_token(identity=user["userId"])
    
    # Log successful login
    logger.info(f"Usuario con ID {user['userId']} ha iniciado sesión exitosamente")
    
    return jsonify({
        "access_token": access_token, 
        "user": get_user_data(user["userId"])
    }), HTTPStatus.OK

@auth_bp.route('/signup', methods=['POST'])
@validate_request_json(['name', 'email', 'password'])
def signup():
    """Register a new user"""
    data = request.json
    name = data.get("name", "").strip()
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")
    rol = data.get("rol", "user").lower().strip()
    
    # Input validation
    if not name or len(name) < 3:
        return jsonify({"msg": "El nombre debe tener al menos 3 caracteres"}), HTTPStatus.BAD_REQUEST
        
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"msg": "Email inválido"}), HTTPStatus.BAD_REQUEST
    
    if not password or len(password) < 8:
        return jsonify({"msg": "La contraseña debe tener al menos 8 caracteres"}), HTTPStatus.BAD_REQUEST
    
    if rol not in ["admin", "user"]:
        return jsonify({"msg": "Rol inválido. Debe ser 'admin' o 'user'"}), HTTPStatus.BAD_REQUEST
    
    db_instance = Database.get_instance()
    users_collection = db_instance.get_collection("users")
    
    # Check if email already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"msg": "Ya existe un usuario con este email"}), HTTPStatus.CONFLICT
    
    # Hash password
    hashed_password = generate_password_hash(password)
    
    # Create user ID
    user_id = str(ObjectId())
    
    # Insert new user
    user_data = {
        "userId": user_id,
        "name": name,
        "email": email,
        "password": hashed_password,
        "rol": rol,
        "created_at": datetime.utcnow()
    }
    
    users_collection.insert_one(user_data)
    
    # Create token for automatic login
    token = create_access_token(identity=user_id)
    
    # Log user creation
    logger.info(f"Nuevo usuario creado con ID {user_id} y rol {rol}")
    
    return jsonify({
        "msg": "Usuario creado exitosamente",
        "access_token": token, 
        "user": get_user_data(user_id)
    }), HTTPStatus.CREATED