from fastapi import FastAPI
from sqlalchemy import text
from connection import SessionFactory

app = FastAPI()

@app.get("/health-check")
def health_check_handler():
    # 컨텍스트 매니지 문법
    with SessionFactory() as session:
        stm = text("SELECT * FROM user LIMIT 1;")
        row = session.execute(stm).fetchone() # Row 객체 반환
    return {"user": row._asdict()}