# Kookmin Feed DB API

이 프로젝트는 `FastAPI`를 사용하여 MongoDB와 상호작용하는 API를 제공합니다.

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install fastapi uvicorn pymongo pydantic
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음과 같은 환경 변수를 설정합니다:

```
MONGODB_URI=mongodb://localhost:27017
DB_NAME=your_db_name
IS_PROD=False
```

### 3. 서버 실행

```bash
uvicorn main:app --reload
```

## API 엔드포인트

### Direct Messages

- **GET /direct-messages/**: 모든 DM 리스트를 반환합니다.
- **POST /direct-messages/**: 새로운 DM을 생성합니다.
  - 요청 본문 예시:
    ```json
    {
      "user_id": "user1",
      "user_name": "User One",
      "scrapers": ["scraper1", "scraper2"]
    }
    ```
- **GET /direct-messages/{user_id}**: 특정 DM을 조회합니다.
- **PUT /direct-messages/{user_id}**: 특정 DM을 업데이트합니다.
  - 요청 본문 예시:
    ```json
    {
      "scrapers": ["scraper3"]
    }
    ```
- **DELETE /direct-messages/{user_id}**: 특정 DM을 삭제합니다.

### Server Channels

- **GET /server-channels/**: 모든 서버 채널 리스트를 반환합니다.
- **POST /server-channels/**: 새로운 서버 채널을 생성합니다.
  - 요청 본문 예시:
    ```json
    {
      "server_id": "server1",
      "server_name": "Server One",
      "channel_id": "channel1",
      "channel_name": "Channel One",
      "scrapers": ["scraper1", "scraper2"]
    }
    ```
- **GET /server-channels/{server_id}**: 특정 서버 채널을 조회합니다.
- **PUT /server-channels/{server_id}**: 특정 서버 채널을 업데이트합니다.
  - 요청 본문 예시:
    ```json
    {
      "scrapers": ["scraper3"]
    }
    ```
- **DELETE /server-channels/{server_id}**: 특정 서버 채널을 삭제합니다.

### Notices

- **GET /notices/{notice_type}**: 특정 공지사항 리스트를 반환합니다.

## 예제

서버를 실행한 후, 브라우저에서 `http://127.0.0.1:8000/docs`로 이동하여 자동 생성된 API 문서를 확인할 수 있습니다.