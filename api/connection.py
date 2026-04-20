# SQLAlchemy connection module

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#              데이터베이스 + 라이브러리 :// 사용자 : 비밀번호 @ 호스트IP주소 : 포트 / 데이터베이스명
DATABASE_URL = "mysql+pymysql://root:password@db:3306/app_db"

# 엔진
engine = create_engine(DATABASE_URL)

# 세션 팩토리
SessionFactory = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)
