# 설명

시간 서비스를 제공하는 Thing 예제.

# 의존성

```bash
pip install -r requirements.txt
```

# 실행

```bash
cd big_thing/clock_big_thing
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

- (없음)

## Value Services

- `current_unix_time -> float`

  현재 유닉스 시간을 제공하는 서비스.

- `current_datetime -> str`

  현재 날짜을 제공하는 서비스.

  - format: `year/month/day`

- `current_time -> str`

  현재 시간을 제공하는 서비스.

  - format: `hour/min/sec`

- `current_year -> int`

  현재 년도를 제공하는 서비스.

- `current_month -> int`

  현재 월을 제공하는 서비스.

- `current_day -> int`

  현재 일을 제공하는 서비스.

- `current_weekday -> str`

  현재 요일을 제공하는 서비스.

  - Monday
  - Tuesday
  - Wednesday
  - Thursday
  - Friday
  - Saturday
  - Sunday
