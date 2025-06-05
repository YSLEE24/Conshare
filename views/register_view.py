from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, jsonify
import pandas as pd
import os
from ..common_store import registered_containers  # 임시 등록 리스트
from Advanced_Conshare.models import Container
from .. import db  # SQLAlchemy 인스턴스

# Blueprint 객체 생성: 'register' 이름으로 등록 관련 라우트를 묶음
register_bp = Blueprint('register', __name__)

# ✅ 1. 등록 폼 페이지 렌더링 (GET 요청 시 HTML 보여줌)
@register_bp.route('/register', methods=['GET'])
def container_register():
    return render_template('container-register.html')

# ✅ 2. 단일 컨테이너 등록 처리 (AJAX POST 요청)
@register_bp.route('/register/submit', methods=['POST'])
def submit():
    # 요청 데이터를 JSON 형식으로 받음
    data = request.get_json()

    # 프론트엔드에서 전송된 데이터 필드 추출
    number = data.get('container_number')       # 컨테이너 번호
    size = data.get('size')                     # 크기 (예: 20FT)
    tare = data.get('tare')                     # 공차무게
    terminal = data.get('terminal')             # 터미널명
    available_from = data.get('available_from') # 사용 가능 시작일
    available_to = data.get('available_to') or None     # 사용 가능 종료일 / 반납 없으면 None
    remarks = data.get('remarks')               # 비고
    price = data.get('price')                   # 가격

    # ✅ 터미널명에 따라 지역과 항만 유형(외항/내항)을 매핑
    region_type_map = {
        'PNIT': ('부산', '외항'), 'PNC': ('부산', '외항'), 'BNCT': ('부산', '외항'),
        'BCT': ('부산', '외항'), 'DGT': ('부산', '외항'), 'HBCT': ('부산', '내항'),
        'BPTG': ('부산', '내항'), 'BPTS': ('부산', '내항'), 'TOC': ('부산', '내항'),
        'SNCT': ('인천', '외항'), 'HJIT': ('인천', '외항'), 'E1CT': ('인천', '내항'),
        'ICT': ('인천', '내항'), 'IFT': ('인천', '내항'), 'KIT': ('광양', '내항'),
        'GWCT': ('광양', '내항'), 'PCTC': ('평택', '내항'), 'PNCT': ('평택', '내항'),
        'JUCT': ('울산', '내항'), 'UNCT': ('울산', '내항'), 'IGCT': ('군산', '내항'),
    }
    region, port_type = region_type_map.get(terminal, ('기타', ''))

    # ✅ SQLAlchemy 모델에 맞춰 새로운 컨테이너 인스턴스 생성
    new_container = Container(
        container_number=number,
        size=size,
        tare=int(tare) if tare else None,
        terminal=terminal,
        region=region,
        type=port_type,
        available_from=available_from,
        available_to=available_to,
        price=int(price) if price else None,
        remarks=remarks
    )

    # ✅ DB에 저장
    db.session.add(new_container)
    db.session.commit()

    # ✅ 성공 메시지를 JSON 형태로 반환
    return jsonify({"message": "등록이 완료되었습니다!"})

# ✅ 3. 등록된 컨테이너 리스트를 보여주는 북킹 페이지
@register_bp.route('/booking', methods=['GET'])
def booking_page():
    return render_template('container-booking.html', containers=registered_containers)

# ✅ 4. 엑셀 등록 템플릿 다운로드
@register_bp.route('/download/template', methods=['GET'])
def download_template():
    return send_from_directory(directory='data_files', path='container_upload_template_final.xlsx', as_attachment=True)

# ✅ 5. 엑셀 파일을 통한 다수 컨테이너 업로드 처리
@register_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    df = pd.read_excel(file)

    region_type_map = {
        'PNIT': ('부산', '외항'), 'PNC': ('부산', '외항'), 'BNCT': ('부산', '외항'),
        'BCT': ('부산', '외항'), 'DGT': ('부산', '외항'), 'HBCT': ('부산', '내항'),
        'BPTG': ('부산', '내항'), 'BPTS': ('부산', '내항'), 'TOC': ('부산', '내항'),
        'SNCT': ('인천', '외항'), 'HJIT': ('인천', '외항'), 'E1CT': ('인천', '내항'),
        'ICT': ('인천', '내항'), 'IFT': ('인천', '내항'), 'KIT': ('광양', '내항'),
        'GWCT': ('광양', '내항'), 'PCTC': ('평택', '내항'), 'PNCT': ('평택', '내항'),
        'JUCT': ('울산', '내항'), 'UNCT': ('울산', '내항'), 'IGCT': ('군산', '내항'),
    }

    for _, row in df.iterrows():
        terminal = row['Terminal']
        region, port_type = region_type_map.get(terminal, ('기타', ''))

        item = {
            "Container Number": row['Container Number'],
            "Size": row['Size'],
            "Tare (kg)": row['Tare'],
            "Terminal": terminal,
            "Region": region,
            "Type": port_type,
            "Available From": row['Available From'],
            "Available To": row['Available To'],
            "Price (KRW)": row['Price'],
            "Remarks": row['Remarks'],
        }
        registered_containers.append(item)

    return redirect(url_for('register.booking_page'))
