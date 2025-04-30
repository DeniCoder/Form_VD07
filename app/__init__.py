from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Убедимся, что instance_path существует
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # Папка уже существует

    # Путь к базе данных
    db_path = os.path.join(app.instance_path, 'site.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    csrf.init_app(app)

    from app.routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app