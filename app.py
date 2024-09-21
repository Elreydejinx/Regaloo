from flask import Flask
from database import init_db
from models import db
from routes import app as app_routes
from flask_mail import Mail

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.ProductionConfig')
    
    init_db(app)
    
    app.register_blueprint(app_routes)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
