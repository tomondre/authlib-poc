from flask import Blueprint, jsonify
from app.utils.jwt_helpers import require_jwt

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/protected', methods=['GET'])
@require_jwt()
def protected(current_user):
    return jsonify({'message': f'Welcome, authorized admin user {current_user}!'})