# 설명

회의록 작성 기능을 제공하는 Thing 예제.

# 의존성

```bash
./setup.sh
```

# 실행

```bash
cd big_thing/conference_big_thing
python run.py
```

# 옵션

- `-n, --name | default = None

  Thing의 이름. 이 이름은 Thing을 구분하기 위한 ID이기도 하다.

- `-ip --host | default='127.0.0.1'`

  Thing의 ip 주소.

- `-p, --port | default=1883`

  Thing의 port 번호.

- `-ac, --alive_cycle | default=60`

  Thing의 alive 패킷 전송 주기. alive 패킷을 통해 Middleware가 Thing의 활성화 여부를 파악한다.

- `--log | default=True`

  Thing의 log기능의 활성화 여부.

# Services

## Function Services

- `record_start() -> bool`

  회의를 시작하는 서비스.

- `record_end() -> bool`

  회의를 끝내는 서비스.

- `to_text() -> bool`

  회의 녹음 파일 경로를 받아 text로 변환하는 서비스.

## Value Services

- (없음)
