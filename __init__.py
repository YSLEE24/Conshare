# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user 
from dotenv import load_dotenv
from datetime import timedelta
from .models import User
import os
from .extensions import db, migrate, login_manager

# db = SQLAlchemy()  # 여기서만 인스턴스 생성
# migrate = Migrate()
# login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('SECRET_KEY') # 세션 보안 키 설정
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    db.init_app(app)
    migrate.init_app(app, db)

    # LoginManager 초기화
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # 로그인 안 했을 때 이동할 뷰
    login_manager.login_message = '로그인이 필요합니다.'
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        # from .models import User
        # return User.query.get(int(user_id))
        print(f"🔍 user_loader 호출됨: user_id={user_id}")
        user = User.query.get(int(user_id)) if user_id else None
        print(f"🔍 user_loader 반환: {user}")
        return user

    # models 지우면 orm에서 모델 못찾음
    from . import models
    from .views import chatbot_view

    # 블루프린트 등록
    from .views import main_view, booking_view, register_view, booked_view, admin_view, auth_view, message_view
    app.register_blueprint(main_view.main_bp)
    app.register_blueprint(booking_view.booking)
    app.register_blueprint(register_view.register_bp)
    app.register_blueprint(booked_view.booked_bp)
    app.register_blueprint(chatbot_view.chatbot_bp)
    app.register_blueprint(admin_view.admin_bp)
    app.register_blueprint(auth_view.auth_bp)
    app.register_blueprint(message_view.message_bp)

    return app