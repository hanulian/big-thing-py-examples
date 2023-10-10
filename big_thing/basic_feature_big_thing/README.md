# 설명

기본적인 big thing의 기능을 사용해보기 위한 예제 thing 코드.

# 실행

```bash
cd big_thing/basic_feature_big_thing
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

- `func_no_arg() -> int`

  랜덤한 정수 값을 반환하는 서비스.

- `func_with_arg(int) -> int`

  정수 값을 인자로 받아 그대로 반환하는 서비스.

- `func_with_arg_and_delay(int, float) -> int`

  정수 값과 지연 시간을 인자로 받아 주어진 시간동안 지연된 후 정수 값을 반환하는 서비스.

## Value Services

- `value_current_time() -> int`

  현재 시간을 10초마다 제공하는 서비스.
