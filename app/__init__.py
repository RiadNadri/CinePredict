from flask import Flask
from app.routes import routes  # Importer le blueprint des routes

def create_app():
    app = Flask(__name__, template_folder="app/templates")
    
    # Enregistrer le blueprint
    app.register_blueprint(routes)
    
    return app
