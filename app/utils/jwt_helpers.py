from functools import wraps
from flask import request, jsonify, current_app
from authlib.jose import jwt, JoseError

def generate_jwt(payload, secret, algorithm):
    return jwt.encode({'alg': algorithm}, payload, secret).decode('utf-8')

def require_jwt(role=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing or invalid token'}), 401
            token = auth_header.split(' ')[1]
            try:
                claims = jwt.decode(token, current_app.config['SECRET_KEY'])
                claims.validate()
                if role and claims.get('role') != role:
                    return jsonify({'error': 'Forbidden'}), 403
            except JoseError as e:
                return jsonify({'error': str(e)}), 401
            return fn(*args, **kwargs)
        return wrapper
    return decorator

