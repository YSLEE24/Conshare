# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()  # 여기서만 인스턴스 생성
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    # 블루프린트 등록
    from .views import main_view, booking_view, register_view, booked_view
    app.register_blueprint(main_view.main_bp)
    app.register_blueprint(booking_view.booking)
    app.register_blueprint(register_view.register_bp)
    app.register_blueprint(booked_view.booked_bp)

    return app