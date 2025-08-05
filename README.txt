# 🧭 ConShare - 컨테이너 자동 중개 및 예약 플랫폼

**ConShare**는 항만 및 물류 산업에서 컨테이너 공유/중개/예약을 효율적으로 관리할 수 있도록 돕는 웹 기반 ERP 시스템입니다.  
예약 시스템, 컨테이너 등록, 자동 중개 알고리즘, 수급 예측 기능 등을 제공합니다.

---

## 📌 기술 스택

| 항목       | 사용 기술                                       |
|------------|------------------------------------------------|
| 백엔드     | Python, Flask, SQLAlchemy                      |
| 데이터베이스 | PostgreSQL                                     |
| 마이그레이션 | Flask-Migrate                                  |
| 프론트엔드  | HTML5, CSS3, JavaScript (Jinja2 템플릿 기반)     |
| 기타       | Pandas, Openpyxl, Bootstrap, Jquery            |
| 실행 환경   | Windows / Mac / Linux                          |

---

## 🚀 설치 및 실행 가이드

### 1. PostgreSQL 설치 및 DB 생성

```sql
-- PostgreSQL 환경에 접속 후 아래 명령 실행
CREATE DATABASE conshare_db;
CREATE USER postgres WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE conshare_db TO postgres;
```

> DB 이름과 사용자, 비밀번호를 위 설정에 맞추지 않으면, `__init__.py`에서 연결 에러가 발생합니다.

---

### 2. 프로젝트 클론 및 의존성 설치

```bash
pip install -r requirements.txt
```

---

### 3. 환경 변수 설정

#### (Windows)

```bash
set FLASK_APP=run.py
set FLASK_ENV=development
```

#### (Mac/Linux)

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

---

### 4. DB 마이그레이션 반영

```bash
flask db upgrade
```

> `migrations/` 폴더가 있어야 하며, 없다면 `flask db init`, `flask db migrate`부터 실행해야 합니다.

---

### 5. 초기 더미 데이터 삽입

```bash
python init_db.py
```

> 내부에 `dummy_container_data_10000.csv` 또는 다른 CSV가 연결되어 있어야 합니다.

---

### 6. Flask 앱 실행

```bash
flask run
```

> 실행 후 `http://localhost:5000` 접속

---

## 📁 주요 폴더 구조

```
.
├── app/
│   ├── templates/              # HTML 템플릿
│   ├── static/                 # CSS, JS, 이미지 등
│   ├── views/                  # 라우팅 및 뷰 함수들
│   ├── models.py               # SQLAlchemy 모델 정의
│   └── __init__.py             # Flask 앱 초기화 및 DB 연결
├── init_db.py                  # 초기 더미 데이터 삽입 스크립트
├── run.py                      # 앱 실행 진입점
├── requirements.txt            # 의존성 리스트
├── migrations/                 # 마이그레이션 관련 파일
└── README.md
```

---

## 💡 참고사항

- DB 연결 문자열은 `__init__.py` 내 다음 구조로 설정되어 있습니다:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/conshare_db'
```

- DB 설정이 다를 경우, 본인 환경에 맞게 URI를 변경해 주세요.

---

## 📝 프로젝트 상태

- 이 프로젝트는 **1인 개발 중**이며, 현재 결제 기능은 포함되어 있지 않습니다.
- 일부 기능은 Flask 기반의 프로토타이핑이며, 향후 FastAPI 또는 Django로 확장 가능성도 고려 중입니다.

---

## 📝 라이센스

MIT License
