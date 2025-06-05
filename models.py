from datetime import datetime
from . import db
from flask_sqlalchemy import SQLAlchemy

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
    release_reference = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 💡 컨테이너 등록자
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='owned_containers')  # backref 이름도 다르게

# 예약 내역용
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    container_id = db.Column(db.Integer, db.ForeignKey('containers.id'), nullable=False)

    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    booked_date = db.Column(db.DateTime, default=datetime.utcnow)

    # 등록 당시 컨테이너 정보 전체 저장
    container_number = db.Column(db.String(20), nullable=False)
    release_reference = db.Column(db.String(100))
    size = db.Column(db.String(10))
    tare = db.Column(db.Integer)
    terminal = db.Column(db.String(50))
    available_from = db.Column(db.Date)
    available_to = db.Column(db.Date)
    remarks = db.Column(db.Text)
    damaged = db.Column(db.Boolean)

    # 관계 설정
    container = db.relationship('Container', backref='bookings')


# 유저 등록

class User(db.Model):
    __tablename__ = 'user'  # 💡 ForeignKey('user.id')와 정확히 일치시켜야 함

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)