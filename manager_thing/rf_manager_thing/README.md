# 예제 설명

MySSIX 시스템에서 Thing의 기본적인 기능을 테스트 해볼 수 있는 Thing 예제

# 실행

```bash
python run.py
```

# 옵션

- `-n, --name | default = None`
  Thing의 이름. 이 이름은 Thing을 구분하기위한 ID이기도 하다
- `-ip --host | default='127.0.0.1'`
  Thing의 ip 주소
- `-p, --port | default=1883`
  Thing의 port 번호
- `-ac, --alive_cycle | default=60`
  Thing의 alive 패킷 전송 주기. alive 패킷을 통해 Middleware가 Thing의 활성화 여부를 파악한다.
- `--log | default=True`
  Thing의 log기능의 활성화 여부.

# Services

## Function Services

- `func_no_arg(None) -> int`
  기본적인 형태의 파라미터가 없는 Function 서비스. 0~100 중에서 랜덤한 숫자를 골라 반환한다.
- `func_with_arg(int) -> int`
  기본적인 형태의 파라미터가 있는 Function 서비스. 정수형 인자를 받아 그대로 반환한다.
- `func_with_arg_and_delay(int, float) -> int`
  기본적인 형태의 파라미터를 받아 인자의 숫자 만큼 sleep하는 Function 서비스. 정수형 인자를 받아 그대로 반환한다

## Value Services

- `value_current_time`
  현재 시간을 알려주는 Value 서비스
