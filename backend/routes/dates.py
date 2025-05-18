# routes/dates.py - Routes for appointments
from flask import Blueprint, request, jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
import datetime
import re
import logging

from db import Database
from utils import admin_required, validate_request_json, paginate_results

dates_bp = Blueprint('dates', __name__)
admin_dates_bp = Blueprint('admin_dates', __name__)
logger = logging.getLogger(__name__)

# Helper functions
def validate_date_format(date_str):
    """Validate date string format (YYYY-MM-DD)"""
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time_format(time_str):
    """Validate time string format (HH:MM)"""
    return bool(re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", time_str))

def date_exists(date_id):
    """Check if date with given ID exists"""
    db_instance = Database.get_instance()
    dates_collection = db_instance.get_collection("dates")
    return dates_collection.count_documents({"_id": ObjectId(date_id)}) > 0

def is_date_owner(date_id, user_id):
    """Check if user is the owner of the date"""
    db_instance = Database.get_instance()
    dates_collection = db_instance.get_collection("dates")
    return dates_collection.count_documents({"_id": ObjectId(date_id), "userId": user_id}) > 0

# User Routes
@dates_bp.route('', methods=['POST'])
@jwt_required()
@validate_request_json(['date', 'time', 'description'])
def create_date():
    """Create a new appointment"""
    user_id = get_jwt_identity()
    data = request.json
    
    # Check if title is valid
    if not data["title"] or len(data["title"]) < 5:
        return jsonify({"msg": "El título debe tener al menos 5 caracteres"}), HTTPStatus.BAD_REQUEST
    
    # Validate date and time formats
    if not validate_date_format(data["date"]):
        return jsonify({"msg": "Formato de fecha inválido. Use YYYY-MM-DD"}), HTTPStatus.BAD_REQUEST
    
    if not validate_time_format(data["time"]):
        return jsonify({"msg": "Formato de hora inválido. Use HH:MM (24h)"}), HTTPStatus.BAD_REQUEST
    
    # Check if date is in the future
    date_obj = datetime.datetime.strptime(f"{data['date']} {data['time']}", "%Y-%m-%d %H:%M")
    if date_obj < datetime.datetime.now():
        return jsonify({"msg": "La cita debe ser en el futuro"}), HTTPStatus.BAD_REQUEST
    
    # Check if time slot is available
    db_instance = Database.get_instance()
    dates_collection = db_instance.get_collection("dates")
    
    existing_date = dates_collection.find_one({
        "date": data["date"],
        "time": data["time"],
        "status": {"$ne": "cancelled"}
    })
    
    if existing_date:
        return jsonify({"msg": "Este horario ya está ocupado"}), HTTPStatus.CONFLICT
    
    # Create new date
    new_date = {
        "userId": user_id,
        "title": data["title"],
        "date": data["date"],
        "time": data["time"],
        "description": data["description"],
        "status": "pending",
        "created_at": datetime.datetime.now()
    }
    
    result = dates_collection.insert_one(new_date)
    
    # Log date creation
    logger.info(f"Nueva cita creada con ID {result.inserted_id} para usuario {user_id}")
    
    return jsonify({
        "msg": "Cita creada exitosamente",
        "date": Database.fix_id({**new_date, "_id": result.inserted_id})
    }), HTTPStatus.CREATED

@dates_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def cancel_date(id):
    """Cancel an appointment"""
    user_id = get_jwt_identity()
    
    # Validate ID format
    try:
        date_id = ObjectId(id)
    except:
        return jsonify({"msg": "ID de cita inválido"}), HTTPStatus.BAD_REQUEST
    
    db_instance = Database.get_instance()
    dates_collection = db_instance.get_collection("dates")
    
    # Check if date exists and belongs to user
    date = dates_collection.find_one({"_id": date_id})
    if not date:
        return jsonify({"msg": "Cita no encontrada"}), HTTPStatus.NOT_FOUND
    
    # Check if user is the owner of the date or an admin
    users_collection = db_instance.get_collection("users")
    user = users_collection.find_one({"userId": user_id})
    
    if date["userId"] != user_id and (not user or user.get("rol") != "admin"):
        return jsonify({"msg": "No tiene permiso para cancelar esta cita"}), HTTPStatus.FORBIDDEN
    
    # Check if date is already cancelled or completed
    if date["status"] != "pending":
        return jsonify({"msg": f"No se puede cancelar una cita con estado: {date['status']}"}), HTTPStatus.BAD_REQUEST
    
    # Update date status
    result = dates_collection.update_one(
        {"_id": date_id},
        {"$set": {"status": "cancelled", "cancelled_at": datetime.datetime.now()}}
    )
    
    # Log date cancellation
    logger.info(f"Cita con ID {id} cancelada por usuario {user_id}")
    
    return jsonify({"msg": "Cita cancelada exitosamente"}), HTTPStatus.OK

# Admin Routes
@admin_dates_bp.route('', methods=['GET'])
@admin_required
def get_all_dates():
    """Get all appointments (admin only)"""
    # Get query parameters
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    status = request.args.get('status')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Build query
    query = {}
    
    # Filter by status if provided
    if status:
        query["status"] = status
    
    # Filter by date range if provided
    if date_from or date_to:
        date_query = {}
        if date_from:
            date_query["$gte"] = date_from
        if date_to:
            date_query["$lte"] = date_to
        query["date"] = date_query
    
    # Get paginated results
    result = paginate_results(
        collection="dates", 
        query=query, 
        page=page, 
        page_size=page_size,
        sort_by=("date", 1)  # Sort by date ascending
    )
    
    return jsonify(result), HTTPStatus.OK

@admin_dates_bp.route('/<id>', methods=['PUT'])
@admin_required
def update_date(id):
    """Update an appointment (admin only)"""
    data = request.json
    
    # Validate ID format
    try:
        date_id = ObjectId(id)
    except:
        return jsonify({"msg": "ID de cita inválido"}), HTTPStatus.BAD_REQUEST
    
    db_instance = Database.get_instance()
    dates_collection = db_instance.get_collection("dates")
    
    # Check if title is valid if provided
    if "title" in data and (not data["title"] or len(data["title"]) < 5):
        return jsonify({"msg": "El título debe tener al menos 5 caracteres"}), HTTPStatus.BAD_REQUEST
    
    # Check if date exists
    if not date_exists(id):
        return jsonify({"msg": "Cita no encontrada"}), HTTPStatus.NOT_FOUND
    
    # Validate date and time formats if provided
    if "date" in data and not validate_date_format(data["date"]):
        return jsonify({"msg": "Formato de fecha inválido. Use YYYY-MM-DD"}), HTTPStatus.BAD_REQUEST
    
    if "time" in data and not validate_time_format(data["time"]):
        return jsonify({"msg": "Formato de hora inválido. Use HH:MM (24h)"}), HTTPStatus.BAD_REQUEST
    
    # Check if description is valid if provided
    if "description" in data and (not data["description"] or len(data["description"]) < 5):
        return jsonify({"msg": "La descripción debe tener al menos 5 caracteres"}), HTTPStatus.BAD_REQUEST
    
    # Check if status is valid if provided
    if "status" in data and data["status"] not in ["pending", "completed", "cancelled"]:
        return jsonify({"msg": "Estado inválido. Debe ser 'pending', 'completed' o 'cancelled'"}), HTTPStatus.BAD_REQUEST
    
    # Add updated_at timestamp
    data["updated_at"] = datetime.datetime.now()
    
    # Update date
    result = dates_collection.update_one(
        {"_id": date_id},
        {"$set": data}
    )
    
    # Log date update
    user_id = get_jwt_identity()
    logger.info(f"Cita con ID {id} actualizada por admin {user_id}")
    
    return jsonify({"msg": "Cita actualizada exitosamente"}), HTTPStatus.OK

@admin_dates_bp.route('/<id>/complete', methods=['PUT'])
@admin_required
def complete_date(id):
    """Mark an appointment as completed (admin only)"""
    # Validate ID format
    try:
        date_id = ObjectId(id)
    except:
        return jsonify({"msg": "ID de cita inválido"}), HTTPStatus.BAD_REQUEST
    
    db_instance = Database.get_instance()
    dates_collection = db_instance.get_collection("dates")
    
    # Check if date exists
    date = dates_collection.find_one({"_id": date_id})
    if not date:
        return jsonify({"msg": "Cita no encontrada"}), HTTPStatus.NOT_FOUND
    
    # Check if date is already completed or cancelled
    if date["status"] != "pending":
        return jsonify({"msg": f"No se puede completar una cita con estado: {date['status']}"}), HTTPStatus.BAD_REQUEST
    
    # Update date status
    result = dates_collection.update_one(
        {"_id": date_id},
        {"$set": {"status": "completed", "completed_at": datetime.datetime.now()}}
    )
    
    # Log date completion
    user_id = get_jwt_identity()
    logger.info(f"Cita con ID {id} marcada como completada por admin {user_id}")
    
    return jsonify({"msg": "Cita marcada como completada exitosamente"}), HTTPStatus.OK

@admin_dates_bp.route('/<id>/cancel', methods=['PUT'])
@admin_required
def cancel_date(id):
    """Cancelar una cita (solo admin)"""
    # Validar formato de ID
    try:
        date_id = ObjectId(id)
    except:
        return jsonify({"msg": "ID de cita inválido"}), HTTPStatus.BAD_REQUEST

    db_instance = Database.get_instance()
    dates_collection = db_instance.get_collection("dates")

    # Verificar que la cita exista
    date = dates_collection.find_one({"_id": date_id})
    if not date:
        return jsonify({"msg": "Cita no encontrada"}), HTTPStatus.NOT_FOUND

    # Verificar que aún no esté cancelada o completada
    if date["status"] != "pending":
        return jsonify({"msg": f"No se puede cancelar una cita con estado: {date['status']}"}), HTTPStatus.BAD_REQUEST

    # Actualizar estado a cancelada
    result = dates_collection.update_one(
        {"_id": date_id},
        {"$set": {"status": "cancelled", "cancelled_at": datetime.datetime.now()}}
    )

    # Registrar en logs
    user_id = get_jwt_identity()
    logger.info(f"Cita con ID {id} cancelada por admin {user_id}")

    return jsonify({"msg": "Cita cancelada exitosamente"}), HTTPStatus.OK
