from flask import Flask

def create_app():
    app = Flask(__name__)

    from .config import Config
    app.config.from_object(Config)

    from .routes.auth import auth_bp
    from .routes.protected import protected_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(protected_bp)

    return app
