# 설명

Big Thing의 모든 서비스 예제를 제공하는 Thing 예제.

# 실행

```bash
cd big_thing/full_feature_big_thing
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

- `--log | default=True`

  Thing의 log기능의 활성화 여부.

# Services

## Function Services

- `fail_function() -> int`

  예외가 발생하는 서비스

- `int_function_no_arg_timeout_3() -> int`

  3초 후에 TIMEOUT 타입 에러를 반환하는 서비스.

- `int_function_no_arg_with_delay_1() -> int`

  인자가 없고 int 값을 1초 후에 반환하는 서비스. 반환 값은 호출 마다 1씩 늘어난다.

- `int_function_no_arg() -> int`

  인자가 없고 int 값을 반환하는 서비스. 반환 값은 호출 마다 1씩 늘어난다.

- `float_function_no_arg() -> int`

  인자가 없고 float 값을 반환하는 서비스. 반환 값은 호출 마다 1씩 늘어난다.

- `str_function_no_arg() -> int`

  인자가 없고 str 값을 반환하는 서비스. 반환 값은 호출 마다 1씩 늘어난 숫자 문자열을 반환한다.

- `bool_function_no_arg() -> int`

  인자가 없고 bool 값을 반환하는 서비스. 반환 값은 호출 마다 반전 된다.

- `binary_function_no_arg() -> int`

  인자가 없고 binary 값을 반환하는 서비스. 반환 값은 호출 마다 1씩 늘어난 숫자 문자열을 base64로 변환한 값을 반환한다.

- `void_function_no_arg() -> int`

  인자가 없고 반환 값도 없는 서비스.

- `int_function_no_arg(int_arg: int) -> int`

  int형 인자를 받아 그대로 int 값을 반환하는 서비스.

- `float_function_no_arg(float_arg: float) -> int`

  float형 인자를 받아 그대로 float 값을 반환하는 서비스.

- `str_function_no_arg(str_arg: str) -> int`

  str형 인자를 받아 그대로 str 값을 반환하는 서비스.

- `bool_function_no_arg(bool_arg: bool) -> int`

  bool형 인자를 받아 그대로 bool 값을 반환하는 서비스.

- `binary_function_no_arg(binary_arg: str) -> int`

  binary형 인자를 받아 그대로 binary 값을 반환하는 서비스.

- `void_function_no_arg(int_arg: int, float_arg: float, str_arg: str, bool_arg: bool, binary_arg: str) -> int`

  int, float, str, bool, binary형 인자를 받아 출력하는 서비스.

## Value Services

- `int_value_5: int`

  5를 고정값으로 가지는 서비스.

- `int_value: int`

  1초마다 1씩 늘어가는 int값을 가지는 서비스.

- `float_value: int`

  1초마다 1.0씩 늘어가는 float값을 가지는 서비스.

- `str_value: int`

  1초마다 1씩 늘어가는 숫자의 문자열값을 가지는 서비스.

- `bool_value: int`

  1초마다 반전되는 bool값을 가지는 서비스.

- `binary_value: int`

  1초마다 1씩 늘어가는 숫자의 문자열값을 base64로 변환한 값을 가지는 서비스.
