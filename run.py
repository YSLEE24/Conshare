# run.py
from Advanced_Conshare import create_app, db
from flask_migrate import Migrate

# 앱 생성
app = create_app()

# Flask-Migrate 등록
migrate = Migrate(app, db)

# 모델 인식: Alembic이 테이블 구조를 인식하려면 models import 필요
from Advanced_Conshare import models