# Kookmin Feed Database API Server

이 프로젝트는 FastAPI를 사용하여 Discord 관련 데이터를 관리하는 API 서버입니다. MongoDB를 데이터베이스로 사용하며, 환경 변수 기반의 설정과 API 키 인증을 지원합니다.

## 주요 기능

- Discord Direct Message 관리
  - Direct Message 목록 조회
  - Direct Message 생성, 조회, 수정, 삭제
- Discord Server Channel 관리
  - Server Channel 목록 조회
  - Server Channel 생성, 조회, 수정, 삭제
- 공지사항 관리
  - 공지사항 목록 조회
  - 새로운 공지사항 조회

## 설치 및 실행

### 1. 의존성 설치

아래 명령어를 사용하여 필요한 Python 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 또는 `envs/.dev.env` 파일을 생성하고 아래와 같은 환경 변수를 설정합니다.

```env
MONGODB_URI=mongodb://<your_mongodb_uri>
DB_NAME=<your_database_name>
API_KEY=<your_api_key>
```

- `MONGODB_URI`: MongoDB 연결 URI
- `DB_NAME`: 기본 데이터베이스 이름
- `API_KEY`: API 인증에 사용할 키

### 3. 서버 실행

아래 명령어를 사용하여 서버를 실행합니다.

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API 사용법

### 인증

모든 API 요청은 `Authorization` 헤더를 통해 인증해야 합니다. 헤더 값은 `Bearer <your_api_key>` 형식이어야 합니다. 올바른 API 키가 제공되지 않으면 403 Forbidden 응답이 반환됩니다.

### 엔드포인트

#### 1. Discord Direct Messages

- **GET /discord/direct-messages**
  - Direct Message 목록 조회
  - 예제:
    ```bash
    curl -X GET "http://localhost:8000/discord/direct-messages" \
    -H "Authorization: Bearer <your_api_key>"
    ```

- **POST /discord/direct-messages**
  - Direct Message 생성
  - 예제:
    ```bash
    curl -X POST "http://localhost:8000/discord/direct-messages" \
    -H "Authorization: Bearer <your_api_key>" \
    -H "Content-Type: application/json" \
    -d '{"user_id": "12345", "user_name": "JohnDoe", "scrapers": ["scraper1", "scraper2"]}'
    ```

- **GET /discord/direct-messages**
  - 특정 Direct Message 조회
  - 예제:
    ```bash
    curl -X GET "http://localhost:8000/discord/direct-messages?user_id=12345" \
    -H "Authorization: Bearer <your_api_key>"
    ```

- **PUT /discord/direct-messages**
  - Direct Message 수정
  - 예제:
    ```bash
    curl -X PUT "http://localhost:8000/discord/direct-messages" \
    -H "Authorization: Bearer <your_api_key>" \
    -H "Content-Type: application/json" \
    -d '{"user_id": "12345", "scrapers": ["scraper3"]}'
    ```

- **DELETE /discord/direct-messages**
  - Direct Message 삭제
  - 예제:
    ```bash
    curl -X DELETE "http://localhost:8000/discord/direct-messages?user_id=12345" \
    -H "Authorization: Bearer <your_api_key>"
    ```

#### 2. Discord Server Channels

- **GET /discord/server-channels**
  - Server Channel 목록 조회
  - 예제:
    ```bash
    curl -X GET "http://localhost:8000/discord/server-channels" \
    -H "Authorization: Bearer <your_api_key>"
    ```

- **POST /discord/server-channels**
  - Server Channel 생성
  - 예제:
    ```bash
    curl -X POST "http://localhost:8000/discord/server-channels" \
    -H "Authorization: Bearer <your_api_key>" \
    -H "Content-Type: application/json" \
    -d '{"server_id": "server123", "server_name": "TestServer", "channel_id": "channel123", "channel_name": "General", "scrapers": ["scraper1"]}'
    ```

- **GET /discord/server-channels**
  - 특정 Server Channel 조회
  - 예제:
    ```bash
    curl -X GET "http://localhost:8000/discord/server-channels?server_id=server123" \
    -H "Authorization: Bearer <your_api_key>"
    ```

- **PUT /discord/server-channels**
  - Server Channel 수정
  - 예제:
    ```bash
    curl -X PUT "http://localhost:8000/discord/server-channels" \
    -H "Authorization: Bearer <your_api_key>" \
    -H "Content-Type: application/json" \
    -d '{"server_id": "server123", "scrapers": ["scraper2"]}'
    ```

- **DELETE /discord/server-channels**
  - Server Channel 삭제
  - 예제:
    ```bash
    curl -X DELETE "http://localhost:8000/discord/server-channels?server_id=server123" \
    -H "Authorization: Bearer <your_api_key>"
    ```

#### 3. Notices

- **GET /notices/all**
  - 공지사항 목록 조회
  - 예제:
    ```bash
    curl -X GET "http://localhost:8000/notices/all?notice_type=general&list_size=5" \
    -H "Authorization: Bearer <your_api_key>"
    ```

- **GET /notices/new**
  - 새로운 공지사항 조회
  - 예제:
    ```bash
    curl -X GET "http://localhost:8000/notices/new?notice_type=general&last_notice_link=https://example.com/notice123" \
    -H "Authorization: Bearer <your_api_key>"
    ```

## 개발 환경

- Python >= 3.8
- FastAPI
- MongoDB
- Python-dotenv