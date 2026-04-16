FROM python:3.13-slim
WORKDIR /app

# 앞에있는건 호스트의 파일, 뒤에있는건 컨테이너의 파일(.은 현재 디렉토리인 /app을 의미) 
COPY . .

# 이미지 빌드할 때 필요한 패키지 설치(이미지 만들때 자동 실행됨)
RUN pip install -r requirements.txt

# 컨테이너 실행할 때 필요한 명령어 설정(컨테이너 실행할 때 자동 실행됨)
# CMD ["fastapi", "dev"] <- 로컬로 실행하는건데, 도커는 127.0.0.1 로컬로 한정되므로 
# 모든 IP에서 접근할 수 있도록 0.0.0.0으로 변경
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# --port <로컬>:<컨테이너> 형식으로 포트 포워딩 설정
