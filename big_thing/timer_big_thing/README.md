# 설명

타이머 서비스를 제공하는 Thing 예제

# 실행

```bash
cd big_thing/timer_big_thing
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

- `timer_set -> float`

  타이머를 초기화하는 서비스.

- `timer_start -> bool`

  타이머를 시작하는 서비스.

## Value Services

- `is_timer_set -> bool`
  타이머가 끝났는지 여부를 제공하는 서비스. `wait until()` 구문 안에 넣어서 사용한다.
