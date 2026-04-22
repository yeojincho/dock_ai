# LLM Chat API

로컬 LLM(Llama)을 활용한 스트리밍 채팅 API 서버입니다. Docker Compose로 API 서버, Worker, MySQL, Redis를 함께 실행합니다.

## 아키텍처

```
클라이언트
    │
    ▼
[API 서버 - FastAPI]  ──── Redis Queue (lpush) ────▶  [Worker - llama-cpp]
    │                                                        │
    │◀─────── Redis Pub/Sub (토큰 스트리밍) ─────────────────┘
    │
    ▼
[MySQL - 대화/메시지 저장]
```

| 서비스 | 역할 | 포트 |
|--------|------|------|
| api | FastAPI 기반 REST API 서버 | 8000 |
| worker | llama-cpp로 LLM 추론 후 Redis에 토큰 publish | - |
| db | MySQL 8.0 (대화, 메시지 영구 저장) | 33061 |
| redis | 작업 큐 및 Pub/Sub 채널 | - |

## 시작하기

### 사전 요구사항

- Docker & Docker Compose
- Llama 모델 파일: `worker/models/Llama-3.2-1B-Instruct-Q4_K_M.gguf`

### 환경변수 설정

```bash
cp .env.example .env
# .env 파일에서 MYSQL_ROOT_PASSWORD, MYSQL_DATABASE 값을 설정
```

### 실행

```bash
docker compose up --build
```

## API

### 새 대화 생성

```
POST /conversations
```

**응답**
```json
{
  "id": "uuid",
  "created_at": "2026-01-01T00:00:00"
}
```

### 메시지 전송 (스트리밍)

```
POST /conversations/{conversation_id}/messages
Content-Type: application/json

{
  "user_input": "안녕하세요!"
}
```

**응답**: `text/event-stream` 형식으로 LLM 토큰을 순차적으로 스트리밍합니다.

> API 문서(Swagger UI): http://localhost:8000/docs

## 프로젝트 구조

```
.
├── docker-compose.yml
├── .env.example
├── api/
│   ├── Dockerfile
│   ├── main.py              # FastAPI 라우터
│   ├── models.py            # SQLAlchemy ORM 모델 (Conversation, Message)
│   ├── connection_async.py  # 비동기 DB 세션 설정
│   └── requirements.txt
└── worker/
    ├── Dockerfile
    ├── main.py              # Redis 큐 소비 + LLM 추론 + Pub/Sub 발행
    ├── requirements.txt
    └── models/
        └── Llama-3.2-1B-Instruct-Q4_K_M.gguf
```

## 데이터 모델

- **Conversation**: 대화 세션 (UUID, 생성일시)
- **Message**: 각 발화 (conversation_id FK, role: user/assistant, content, 생성일시)

MySQL 데이터는 Docker named volume(`local_db`)에 저장되어 컨테이너 재시작 후에도 유지됩니다.
