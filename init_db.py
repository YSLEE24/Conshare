import pandas as pd
from sqlalchemy import create_engine

# DB 연결 설정 (PostgreSQL용)
username = 'postgres'  # PostgreSQL 기본 사용자명
password = '1234'      # 설치할 때 설정한 비밀번호
host = 'localhost'
port = '5432'
database = 'conshare_db'

# CSV 파일 읽기
df = pd.read_csv('data_files/dummy_container_data_500.csv')

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

# SQLAlchemy PostgreSQL 엔진 생성 (★ psycopg2 사용!)
engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# DB에 저장 (append = 기존 테이블에 추가)
df.to_sql('containers', con=engine, if_exists='append', index=False)

print("✅ CSV 데이터를 PostgreSQL에 성공적으로 업로드했습니다.")