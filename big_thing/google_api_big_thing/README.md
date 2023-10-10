# 설명

Google API 기능을 제공하는 예제. (현재는 Vision API만 지원)

# 의존성

```bash
./setup.sh
```

# 실행

```bash
cd big_thing/google_api_big_thing
python run.py
```

# 옵션

- `-n, --name | default = None`

  Thing의 이름. 이 이름은 Thing을 구분하기 위한 ID이기도 하다.

- `-ip --host | default='127.0.0.1'`

  Thing의 ip 주소.

- `-p, --port | default=1883`

  Thing의 port 번호.

- `-ac, --alive_cycle | default=60`

  Thing의 alive 패킷 전송 주기. alive 패킷을 통해 Middleware가 Thing의 활성화 여부를 파악한다.

- `-as, --auto_scan | default=True`

  Middleware 자동스캔 기능 활성화 여부.

- `--log | default=True`

  Thing의 log기능의 활성화 여부.

# Services

## Function Services

- `detect_face(image_path: str) -> bool`

  `image_path`경로에 있는 이미지에서 하나의 얼굴을 감지 및 감정을 검출하여 반환하는 서비스.

- `recommend_song(emotion_state: str) -> str`

  콤마(`,`)로 구분된 감정 상태 문자열을 인자로 받아 해당 감정에 맞는 음악을 추천하는 서비스.

## Value Services

- (없음)
