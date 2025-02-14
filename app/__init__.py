from flask import Flask
from app.routes import routes  
import secrets



def create_app():
    app = Flask(__name__, template_folder="app/templates")
    app.secret_key = secrets.token_hex(16)  
    app.register_blueprint(routes)
    
    return app
