from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.protected import protected_bp

    app.register_blueprint(protected_bp)

    return app
