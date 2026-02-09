from flask import Flask
from config import Config
from database.db_init import db
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Login manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Register routes
    from routes.auth_routes import auth_bp
    from routes.disclosure_routes import disclosure_bp
    from routes.sharing_routes import sharing_bp
    from routes.recipient_routes import recipient_bp
    from routes.audit_routes import audit_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(disclosure_bp)
    app.register_blueprint(sharing_bp)
    app.register_blueprint(recipient_bp)
    app.register_blueprint(audit_bp)

    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=True)
