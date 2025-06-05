from flask import Blueprint, render_template, request, url_for, redirect, flash
from ..models import db, Container, Booking
from datetime import datetime

booking = Blueprint('booking', __name__, url_prefix='/booking')

@booking.route('/', methods=['GET'])
def container_booking():
    # 예약되지 않은 컨테이너만 조회
    booked_container_ids = db.session.query(Booking.container_id).subquery()
    available_containers = Container.query.filter(~Container.id.in_(booked_container_ids)).all()
    return render_template('container-booking.html', containers=available_containers)

@booking.route('/submit', methods=['POST'])
def submit_booking():
    container_id = request.form.get('container_id')
    user_id = request.form.get('user_id')
    user_name = request.form.get('user_name')

    # 🔒 중복 예약 방지
    if Booking.query.filter_by(container_id=container_id).first():
        flash("이미 예약된 컨테이너입니다.")
        return redirect(url_for("booking.container_booking"))

    # 예약 정보 저장
    booking = Booking(
        container_id=container_id,
        user_id=user_id,
        user_name=user_name,
        booked_date=datetime.utcnow()
    )
    db.session.add(booking)
    db.session.commit()

    flash("예약이 완료되었습니다.")
    return redirect(url_for("booking.container_booking"))
