from functools import wraps
from flask import request, jsonify
from authlib.jose import jwt, JsonWebKey, JoseError

def require_jwt():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing or invalid token'}), 401

            token = auth_header.split(' ')[1]

            try:
                # Fetched from IDP_JWK_URL = "https://iam-escape.cloud.cnaf.infn.it/jwk"
                jwks = {
                    "kty": "RSA",
                    "e": "AQAB",
                    "kid": "rsa1",
                    "n": "mGAOEOB5-SIEw5RBkghiTOnnoDWeTK9AW3LPW_jLCxdl7vLJ9dDyraOie28WzR4DzUVGHdM7cxRBSZYslPD8ZixBn2XdCsgiNkzDxH_2_FO8bFtD0G0apqTbVTeTrEpCptgUmARqh2vLnrpA8niwdNdqKdTII7BUd9NhrUbNLlW39k3htTO-oYXQjCy_AnlKiyre44SKr_xr7xBH4LtfY9O3n_4cAogW8hIOLtJkrYsmyGNGne1foPXvnLPrDn0agddN2VrkeFhOAvPiKIOPrT1kKYV6SIl4nO_sz-VomwQYro3iDd4ZGSA7No42N1yPH3SJyIX3QF0wdQ3JMWDR_w",
                    "alg": "RS256"
                }
                decoded = jwt.decode(token, jwks)

                current_user = decoded.get('sub')
                if not current_user:
                    return jsonify({'error': 'Missing subject in token'}), 401

                kwargs['current_user'] = current_user
                return fn(*args, **kwargs)
            except JoseError as e:
                return jsonify({'error': str(e)}), 401

        return wrapper

    return decorator