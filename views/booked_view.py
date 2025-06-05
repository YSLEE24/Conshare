# 사용자가 upload한 컨테이너 리스트(혹은 내역들 보는 페이지)

from flask import Blueprint, render_template, request, jsonify, session
from ..models import Booking
from .. import db
from datetime import datetime

booked_bp = Blueprint('booked', __name__)

# 예약 내역 조회
@booked_bp.route('/booked')
def show_booked():
    user_id = session.get('user_id')
    results = Booking.query.filter_by(user_id=user_id).all()
    return render_template("container-booked.html", bookings=results)

# 예약 처리
@booked_bp.route('/booked/reserve', methods=['POST'])
def reserve_container():
    try:
        data = request.get_json()

        # Booking 테이블에 저장
        booking = Booking(
            container_number=data.get('container_number'),
            size=data.get('size'),
            tare=data.get('tare'),
            terminal=data.get('terminal'),
            region=data.get('region'),
            type=data.get('type'),
            available_from=datetime.strptime(data.get('available_from'), '%Y-%m-%d'),
            available_to=datetime.strptime(data.get('available_to'), '%Y-%m-%d'),
            price_krw=data.get('price_krw'),
            remarks=data.get('remarks'),
            release_reference=data.get('release_reference'),
            booked_date=datetime.utcnow(),
            user_name=data.get('user_name', 'guest')  # 로그인 기능 없으면 guest
        )
        db.session.add(booking)
        db.session.commit()

        return jsonify({'message': '예약 완료'}), 200
    except Exception as e:
        print(f"[예약 오류] {e}")
        return jsonify({'error': '예약 실패'}), 500
