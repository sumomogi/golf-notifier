# Golf Notifier

Apple 캘린더에 골프 일정이 있으면 지정한 상대방에게 자동으로 iMessage를 보내주는 macOS 자동화 도구입니다.

아침 픽업이 어렵다는 사실을 미리 알릴 수 있습니다. launchd로 백그라운드에서 조용히 실행됩니다.

## 동작 방식

- 매일 저녁 8시 50분에 Apple 캘린더를 확인
- 설정한 `calendar_tag` (예: `"Golf"`)가 포함된 일정을 향후 14일 이내에서 검색
- 세 시점에 iMessage 발송:
  - **7일 전** — `week_before`
  - **직전 주말** (토요일 또는 일요일) — `weekend_before`
  - **전날 밤** — `night_before`
- 중복 방지: 동일 일정·시점에 메시지는 한 번만 발송

## 요구사항

- macOS (Apple 캘린더 + Messages AppleScript 사용)
- Python 3.9 이상
- Messages 앱의 연락처 접근 권한
- 캘린더 접근 권한

## 설치

1. 레포 클론:
   ```bash
   git clone https://github.com/sumomogi/golf-notifier.git
   cd golf-notifier
   ```

2. 설정 파일 복사 후 편집:
   ```bash
   cp config.example.json config.json
   ```
   아래 항목을 채워주세요:
   - `recipient` — E.164 형식 전화번호 (예: `+818012345678`)
   - `recipient_name` — 수신자 이름 (참고용)
   - `calendar_tag` — 일정 제목, 메모, 태그, 또는 캘린더 이름에서 검색할 키워드
   - `locale` — `"en"`, `"ja"`, `"ko"` 중 선택 (요일·날짜 형식에 적용)
   - `messages` — 각 시점의 메시지 문구 커스터마이즈

3. 설치 스크립트 실행 (launchd 등록 및 Mac 자동 기상 설정):
   ```bash
   bash setup.sh
   ```

4. 실제 발송 없이 테스트:
   ```bash
   python3 check_golf_schedule.py --dry-run
   ```

## 설정

```json
{
  "recipient": "+1XXXXXXXXXX",
  "recipient_name": "받는 사람 이름",
  "calendar_tag": "골프",
  "lookahead_days": 14,
  "send_time": "20:50",
  "locale": "ko",
  "messages": {
    "week_before": "안내: 다음 주 {weekday} ({date})에 골프 일정이 있어서 아침에 데려다 드리기 어려울 것 같아요. 미리 알려드립니다!",
    "weekend_before": "안내: 이번 주 {weekday} ({date})에 골프 일정이 있어서 아침 픽업이 어려울 수 있어요. 미리 준비해 주세요.",
    "night_before": "안내: 내일 ({date})에 골프가 있어서 아침에 데려다 드리지 못합니다. 불편을 드려서 죄송합니다!"
  }
}
```

### 로케일 옵션

| `locale` | 요일 예시 | 날짜 예시 |
|----------|-----------|-----------|
| `ko`     | 월요일     | 4월 27일  |
| `ja`     | 月曜日     | 4月27日   |
| `en`     | Monday    | April 27  |

### 템플릿 변수

| 변수         | 설명                      |
|--------------|---------------------------|
| `{weekday}`  | 요일 (로케일에 맞게 표시) |
| `{date}`     | 일정 날짜 (로케일에 맞게 표시) |

## 테스트 실행

```bash
python3 -m pytest tests/ -v
```

## 파일 구조

```
golf_notifier/
├── check_golf_schedule.py          # 메인 실행 파일
├── config.example.json             # 설정 템플릿 (config.json으로 복사해서 사용)
├── golf-notifier.plist.template    # launchd 템플릿 (setup.sh가 경로 자동 치환)
├── setup.sh                        # 최초 설치 스크립트
├── notifier/
│   ├── calendar.py                 # AppleScript로 Apple 캘린더 읽기
│   ├── composer.py                 # 로케일 지원 메시지 포맷터
│   ├── sender.py                   # AppleScript로 iMessage 발송
│   ├── dedup.py                    # 중복 발송 방지
│   └── touchpoints.py              # 오늘 발송해야 할 시점 판단
└── tests/
```

## 라이선스

MIT
