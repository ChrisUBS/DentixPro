# utils.py - Utility functions and middleware
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from http import HTTPStatus
from db import Database

def admin_required(fn):
    """Decorator to check if user has admin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        # Get database instance
        db_instance = Database.get_instance()
        users_collection = db_instance.get_collection("users")
        
        # Check if user exists and has admin role
        user = users_collection.find_one({"userId": user_id})
        if not user or user.get("rol") != "admin":
            return jsonify({"msg": "Acceso denegado: se requieren permisos de administrador"}), HTTPStatus.FORBIDDEN
        
        return fn(*args, **kwargs)
    return wrapper

def validate_request_json(required_fields):
    """Decorator to validate request JSON data"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            data = request.json
            if not data:
                return jsonify({"msg": "Datos JSON requeridos"}), HTTPStatus.BAD_REQUEST
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "msg": f"Campos requeridos faltantes: {', '.join(missing_fields)}"
                }), HTTPStatus.BAD_REQUEST
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def get_user_data(user_id):
    """Get user data from database (excluding sensitive info)"""
    db_instance = Database.get_instance()
    users_collection = db_instance.get_collection("users")
    
    user = users_collection.find_one({"userId": user_id})
    if user:
        return {
            "userId": user["userId"],
            "name": user["name"],
            "email": user.get("email"),
            "rol": user.get("rol")
        }
    return None

def paginate_results(collection, query, page=1, page_size=10, sort_by=None):
    """Helper function to paginate query results"""
    db_instance = Database.get_instance()
    collection = db_instance.get_collection(collection)
    
    # Calculate skip value (for pagination)
    skip = (page - 1) * page_size
    
    # Apply sorting if provided
    cursor = collection.find(query)
    if sort_by:
        cursor = cursor.sort(sort_by[0], sort_by[1])
    
    # Get total count (for pagination metadata)
    total_count = collection.count_documents(query)
    
    # Get paginated results
    results = list(cursor.skip(skip).limit(page_size))
    
    # Fix ObjectIds
    results = Database.fix_ids(results)
    
    # Calculate pagination metadata
    total_pages = (total_count + page_size - 1) // page_size
    
    return {
        "data": results,
        "pagination": {
            "total_items": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size
        }
    }