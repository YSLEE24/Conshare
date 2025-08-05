import pandas as pd
import uuid
from sqlalchemy import create_engine
from datetime import datetime

# DB 연결 설정 (PostgreSQL용)
username = 'postgres'
password = '1234'
host = 'localhost'
port = '5432'
database = 'conshare_db'

# CSV 파일 읽기
df = pd.read_csv('data_files/dummy_container_data_1000.csv')

# 컬럼명 PostgreSQL 테이블에 맞게 정리
df.rename(columns={
    'Container Number': 'container_number',
    'Size': 'size',
    'Tare (kg)': 'tare',
    'Terminal': 'terminal',
    'Region': 'region',
    'Type': 'type',
    'Available From': 'available_from',
    'Available To': 'available_to',
    'Price (KRW)': 'price',
    'Remarks': 'remarks'
}, inplace=True)

# 없는 컬럼에 대해 자동값 생성 및 추가
df['status'] = 'available'

# release_reference는 UUID 문자열로 생성
df['release_reference'] = [str(uuid.uuid4())[:8] for _ in range(len(df))]

# created_at을 현재 시각으로 설정 (등록일자)
df['created_at'] = datetime.utcnow()

# SQLAlchemy PostgreSQL 엔진 생성
engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# DB에 저장 (append = 기존 테이블에 추가)
df.to_sql('containers', con=engine, if_exists='append', index=False)

print("✅ CSV 데이터를 PostgreSQL에 성공적으로 업로드했습니다.")
