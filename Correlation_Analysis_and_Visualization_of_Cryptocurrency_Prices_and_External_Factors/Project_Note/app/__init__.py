from flask import Flask
from app.routes import main_bp, brain_bp, complaint_bp, analysis_bp
from app.auth.routes import auth_bp
from app.db import close_db

def create_app():
    app = Flask(__name__)
    app.secret_key = "JohnYim_Mini_Project_2025@@"
    app.register_blueprint(main_bp)
    app.register_blueprint(brain_bp, url_prefix="/brain")
    app.register_blueprint(complaint_bp, url_prefix="/complaint")
    app.register_blueprint(analysis_bp)
    app.register_blueprint(auth_bp)
    app.teardown_appcontext(close_db)
    return app