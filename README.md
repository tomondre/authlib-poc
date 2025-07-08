# Authlib PoC Flask App

This project is a proof-of-concept (PoC) Flask application demonstrating JWT authentication using INDIGO IAM tokens and public JWK validation. The implementation aligns with the REANA server setup and is intended for secure, token-based access to protected endpoints.

## Features
- JWT authentication for protected endpoints
- Uses INDIGO IAM as the identity provider (IDP)
- Validates JWTs using public JWKs (currently hardcoded for PoC)
- Passes `current_user` to endpoint functions after authentication
- The `require_jwt` decorator is used for endpoint configuration.
- The decorator stores the authenticated user's ID in `current_user`.

## Prerequisites
- [INDIGO IAM](https://iam-escape.cloud.cnaf.infn.it/) account and access to its token endpoint
- Obtain a valid JWT token from INDIGO IAM before accessing protected endpoints

## Running the Application
1. Install dependencies and start the Flask app:
   ```bash
   pip install -r requirements.txt
   python run.py
   ```
   The server will start on the default Flask port (5000).

## Stopping the Application
Press `Ctrl+C` in the terminal where the server is running.

## Authentication & Usage
- All protected endpoints require a valid JWT token issued by INDIGO IAM.
- The token must be included in the `Authorization` header as:
  ```
  Authorization: Bearer <your-jwt-token>
  ```
- Example request (using `curl`):
  ```bash
  curl -H "Authorization: Bearer <your-jwt-token>" http://localhost:5000/protected
  ```
- The JWT token must be exchanged beforehand with the INDIGO IAM IDP. See [INDIGO API documentation](https://indigo-iam.github.io/v/v1.12.0/docs/reference/api/) for details on obtaining a token.
- **Tip:** You can obtain a valid token by inspecting the network requests of an application that consumes INDIGO IAM (such as the ESCAPE IAM deployment); look for the `Authorization` header in authenticated requests.

## Implementation Details
- The app uses the `authlib` library to decode and validate JWTs.
- JWKs for validation are currently hardcoded in the code for demonstration. In production, fetch them dynamically from the INDIGO IAM JWK endpoint (for example, ESCAPE IAM: `https://iam-escape.cloud.cnaf.infn.it/jwk`).
- After successful authentication, the `current_user` (from the JWT `sub` claim) is passed to the endpoint function.
- The implementation closely follows the REANA server's authentication approach.
- The `require_jwt` decorator is used to protect endpoints and injects the authenticated user's ID as `current_user`.

## Notes
- This PoC is for demonstration and development purposes. Do not use hardcoded keys in production.
- For production, always fetch and cache JWKs securely from the INDIGO IAM endpoint.

## License
Apache-2.0
