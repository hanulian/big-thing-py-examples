# 설명

여러가지 센서들의 값을 제공하는 Thing 예제. adafruit사의 tsl2591, bme280, sgp30 모듈등이 필요하다.

# 의존성

```python
pip install -r requirements.txt
```

# 실행

```bash
cd big_thing/sensor_box_big_thing
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
- `-as, --auto_scan | default=True`
  Middleware 자동스캔 기능 활성화 여부.
- `--log | default=True`
  Thing의 log기능의 활성화 여부.

# Services

## Function Services

- (없음)

## Value Services

- `temp -> float`
  온도값을 제공하는 서비스
- `humid -> float`
  습도값을 제공하는 서비스
- `pressure -> float`
  기압값을 제공하는 서비
- `CO2 -> int`
  이산화탄소 농도값을 제공하는 서비스
- `brightness -> int`
  광량값을 제공하는 서비스
- `sound -> int`
  소리크기값을 제공하는 서비스
- `dust -> float`
  미세먼지값을 제공하는 서비스
- `VOC -> float`
  유해가스 농도값을 제공하는 서비스
