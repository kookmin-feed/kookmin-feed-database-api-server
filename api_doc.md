# API 문서

이 문서는 Kookmin Feed Database API Server의 엔드포인트와 사용법을 설명합니다.

## 인증

모든 API 요청은 `Authorization` 헤더를 통해 인증해야 합니다. 헤더 값은 `Bearer <your_api_key>` 형식이어야 합니다. 올바른 API 키가 제공되지 않으면 403 Forbidden 응답이 반환됩니다.

---

## 엔드포인트

### 1. Discord Direct Messages

#### **GET /discord/direct-messages**
- Direct Message 목록 조회
- 예제:
  ```bash
  curl -X GET "http://localhost:8000/discord/direct-messages" \
  -H "Authorization: Bearer <your_api_key>"
  ```

#### **POST /discord/direct-messages**
- Direct Message 생성
- 요청 데이터:
  ```json
  {
    "user_id": "12345",
    "user_name": "JohnDoe",
    "scrapers": ["scraper1", "scraper2"]
  }
  ```
- 예제:
  ```bash
  curl -X POST "http://localhost:8000/discord/direct-messages" \
  -H "Authorization: Bearer <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "12345", "user_name": "JohnDoe", "scrapers": ["scraper1", "scraper2"]}'
  ```

#### **GET /discord/direct-message**
- 특정 Direct Message 조회
- 요청 파라미터: `user_id`
- 예제:
  ```bash
  curl -X GET "http://localhost:8000/discord/direct-message?user_id=12345" \
  -H "Authorization: Bearer <your_api_key>"
  ```

#### **PUT /discord/direct-messages**
- Direct Message 수정
- 요청 데이터:
  ```json
  {
    "user_id": "12345",
    "scrapers": ["scraper3"]
  }
  ```
- 예제:
  ```bash
  curl -X PUT "http://localhost:8000/discord/direct-messages" \
  -H "Authorization: Bearer <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "12345", "scrapers": ["scraper3"]}'
  ```

#### **DELETE /discord/direct-messages**
- Direct Message 삭제
- 요청 파라미터: `user_id`
- 예제:
  ```bash
  curl -X DELETE "http://localhost:8000/discord/direct-messages?user_id=12345" \
  -H "Authorization: Bearer <your_api_key>"
  ```

---

### 2. Discord Server Channels

#### **GET /discord/server-channels**
- Server Channel 목록 조회
- 예제:
  ```bash
  curl -X GET "http://localhost:8000/discord/server-channels" \
  -H "Authorization: Bearer <your_api_key>"
  ```

#### **POST /discord/server-channels**
- Server Channel 생성
- 요청 데이터:
  ```json
  {
    "guild_name": "TestServer",
    "channel_id": "channel123",
    "channel_name": "General",
    "scrapers": ["scraper1"]
  }
  ```
- 예제:
  ```bash
  curl -X POST "http://localhost:8000/discord/server-channels" \
  -H "Authorization: Bearer <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{"guild_name": "TestServer", "channel_id": "channel123", "channel_name": "General", "scrapers": ["scraper1"]}'
  ```

#### **GET /discord/server-channel**
- 특정 Server Channel 조회
- 요청 파라미터: `channel_id`
- 예제:
  ```bash
  curl -X GET "http://localhost:8000/discord/server-channel?channel_id=channel123" \
  -H "Authorization: Bearer <your_api_key>"
  ```

#### **PUT /discord/server-channels**
- Server Channel 수정
- 요청 데이터:
  ```json
  {
    "channel_id": "channel123",
    "scrapers": ["scraper2"]
  }
  ```
- 예제:
  ```bash
  curl -X PUT "http://localhost:8000/discord/server-channels" \
  -H "Authorization: Bearer <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{"channel_id": "channel123", "scrapers": ["scraper2"]}'
  ```

#### **DELETE /discord/server-channels**
- Server Channel 삭제
- 요청 파라미터: `channel_id`
- 예제:
  ```bash
  curl -X DELETE "http://localhost:8000/discord/server-channels?channel_id=channel123" \
  -H "Authorization: Bearer <your_api_key>"
  ```

---

### 3. Notices

#### **GET /notices/all**
- 공지사항 목록 조회
- 요청 파라미터:
  - `notice_type`: 공지사항 유형
  - `list_size`: 조회할 공지사항 개수
- 예제:
  ```bash
  curl -X GET "http://localhost:8000/notices/all?notice_type=general&list_size=5" \
  -H "Authorization: Bearer <your_api_key>"
  ```

#### **GET /notices/new**
- 새로운 공지사항 조회
- 요청 파라미터:
  - `notice_type`: 공지사항 유형
  - `last_notice_link`: 마지막으로 확인한 공지사항 링크
- 예제:
  ```bash
  curl -X GET "http://localhost:8000/notices/new?notice_type=general&last_notice_link=https://example.com/notice123" \
  -H "Authorization: Bearer <your_api_key>"
  ```

---

### 4. Scraper Metadata

#### **GET /scraper/types**
- 스크래퍼 유형 목록 조회
- 예제:
  ```bash
  curl -X GET "http://localhost:8000/scraper/types" \
  -H "Authorization: Bearer <your_api_key>"
  ```

#### **GET /scraper/categories**
- 스크래퍼 카테고리 목록 조회
- 예제:
  ```bash
  curl -X GET "http://localhost:8000/scraper/categories" \
  -H "Authorization: Bearer <your_api_key>"
  ```
