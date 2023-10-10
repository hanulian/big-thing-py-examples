# 설명

음악 재생 기능을 제공하는 Thing 예제.

# 의존성

```bash
./setup.sh
```

# 실행

```bash
cd big_thing/music_player_big_thing
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

- `play(source: str) -> bool`

  인자로 받은 `source`가 재생가능한 파일 경로인 경우 해당 파일을 재생하고, url인 경우 해당 url으로 부터 음악 파일을 스트리밍받아 재생하는 서비스.

- `pause_toggle() -> bool`

  음악이 재생중인 경우 일시정지하고, 멈춰있는 경우 다시 재생하는 서비스.

- `stop() -> bool`

  음악 재생을 중지하는 서비스.

## Value Services

- (없음)
