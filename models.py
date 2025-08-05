from datetime import datetime
from .extensions import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# 컨테이너 테이블
class Container(db.Model):
    __tablename__ = 'containers'

    id = db.Column(db.Integer, primary_key=True)
    container_number = db.Column(db.String(20), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    tare = db.Column(db.Integer)
    terminal = db.Column(db.String(50))
    region = db.Column(db.String(20))
    type = db.Column(db.String(20))
    available_from = db.Column(db.Date)
    available_to = db.Column(db.Date)
    price = db.Column(db.Integer)
    remarks = db.Column(db.Text)

    release_reference = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(20), default='available')  # 예약 가능 상태
    last_booked_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='owned_containers')

# 예약 내역 테이블
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    container_id = db.Column(db.Integer, db.ForeignKey('containers.id'), nullable=False)

    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    booked_date = db.Column(db.DateTime, default=datetime.utcnow)

    # 등록 당시 컨테이너 정보
    container_number = db.Column(db.String(20), nullable=False)
    release_reference = db.Column(db.String(100))
    size = db.Column(db.String(10))
    tare = db.Column(db.Integer)
    terminal = db.Column(db.String(50))
    available_from = db.Column(db.Date)
    available_to = db.Column(db.Date)
    remarks = db.Column(db.Text)
    damaged = db.Column(db.Boolean, default=False)

    # 상태: pending, confirmed, rejected
    status = db.Column(db.String(20), default='pending')

    # 운영자 보기용 필드
    user_email = db.Column(db.String(120))  # 예약자 이메일
    owner_name = db.Column(db.String(50))   # 컨테이너 등록자 이름

    container = db.relationship('Container', backref='bookings')

# 유저 테이블
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # 추가된 필드
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255))
    role = db.Column(db.Enum('owner', 'booker', 'admin', 'both', name='user_role'), default='both')
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 챗봇 히스토리 테이블
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64))
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# 메세지 테이블 (예약용)
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
