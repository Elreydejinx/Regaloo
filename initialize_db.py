from models import create_app, db

app = create_app()
with app.app_context(app):
    db.create_all()