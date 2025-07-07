from flask import Blueprint, request, jsonify, current_app
from app.utils.jwt_helpers import generate_jwt
import time

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/token', methods=['POST'])
def issue_token():
    data = request.get_json()
    username = data.get('username', 'anonymous')
    role = data.get('role', 'user')

    payload = {
        'sub': username,
        'role': role,
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600
    }

    token = generate_jwt(payload, current_app.config['SECRET_KEY'], current_app.config['JWT_ALGORITHM'])
    return jsonify(token=token)
