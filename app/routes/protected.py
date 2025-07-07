from flask import Blueprint, jsonify
from app.utils.jwt_helpers import require_jwt

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/protected', methods=['GET'])
@require_jwt(role='admin')
def protected():
    return jsonify({'message': 'Welcome, authorized admin user!'})
