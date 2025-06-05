1. PostgreSQL 설치 후 DB 생성
   - DB명: conshare_db
   - 사용자명: postgres
   - 비밀번호: 1234

2. 의존성 설치
   pip install -r requirements.txt

3. 환경 변수 설정
   (Windows)
   set FLASK_APP=run.py
   set FLASK_ENV=development

   (Mac/Linux)
   export FLASK_APP=run.py
   export FLASK_ENV=development

4. DB 마이그레이션 반영
   flask db upgrade

5. dummy CSV 데이터 삽입
   python init_db.py

6. Flask 앱 실행
   flask run


!!!! '__init__.py'에서 app.config에 아래와 같은 구조로 해놔서
postgresql+psycopg2://<사용자명>:<비밀번호>@<호스트>:<포트>/<DB이름>

DB설정을 저랑 동일하게 맞추던지 본인거 대로 하던지 하세요


제거랑 맞추는 법 아래처럼 하면 됨(psql에서)
CREATE DATABASE conshare_db;
CREATE USER postgres WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE conshare_db TO postgres;