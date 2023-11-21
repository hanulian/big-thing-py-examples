# 예제 설명

<aside>
💡 우분투에서만 사용가능한 예제입니다.

</aside>

사물 감지 서비스를 제공하는 Thing 예제

# 의존성

```
chmod +x setup.sh
./setup.sh
```

# 실행

```bash
cd big_thing/object_detector_big_thing
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

- `detect_start() -> bool`

  사물 감지를 시작하는 서비스.

- `detect_stop() -> bool`

  사물 감지를 중단하는 서비스.

## Value Services

- `is_detection_running() -> bool`

  사물 감지가 실행중인지 여부를 제공하는 서비스.

- `detected_object() -> bool`

  감지된 사물의 종류와 개수를 제공하는 서비스.

- `person_num() -> bool`

  감지된 사람의 개수를 제공하는 서비스.
