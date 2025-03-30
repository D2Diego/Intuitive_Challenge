from flask import Flask
from flask_cors import CORS
from config.config import Config
from app.controllers.operadora_controller import operadora_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    app.register_blueprint(operadora_bp, url_prefix='/api')
    
    return app 