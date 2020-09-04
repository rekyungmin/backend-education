# Task11
- 2020\-09\-01 (TUE)
- 주제: API Server 입문


## 배우는 내용
- biblebot과 aiohttp를 이용하여 API 서버 만들기

## 사전 요구사항
- aiohttp
- biblebot

## 태스크
biblebot의 [intranet API](https://github.com/rekyungmin/biblebot-scraper/blob/master/docs/APIs.md#Intranet)를 제공하는 API 서버를 구축합니다.   

- 데이터 포맷은 `JSON`으로 합니다.
- HTTP 메서드별 특징을 알아본 뒤, 어떤 메서드를 요청 하는 것이 좋을지 알아보세요: [참고링크](https://developer.mozilla.org/ko/docs/Web/HTTP/Methods)
- 예외적인 상황이 발생했을 때는 어떤 응답 상태 코드를 보낼지도 고민해보세요: [참고링크](https://developer.mozilla.org/ko/docs/Web/HTTP/Status)
- HTTP는 stateless입니다. `chapel`, `timetable`, `course` 기능은 로그인이 필요한 기능인데, 어떻게 로그인 상태를 유지할 수 있을지도 고민해보세요.

**다음의 라우팅 경로에, 해당 기능을 구현하세요:**

| 라우팅 경로  | 기능                                   |
| ------------ | -------------------------------------- |
| `/login`     | 로그인 요청을 합니다.                  |
| `/chapel`    | 채플 데이터를 가져옵니다.              |
| `/timetable` | 시간표 데이터를 가져옵니다.            |
| `/course`    | 수강신청 강의의 상세정보를 가져옵니다. |


