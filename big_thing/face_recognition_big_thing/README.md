# 설명

인물 인식 기능을 제공하는 Thing 예제.

# 실행

```bash
cd big_thing/face_recognition_big_thing
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

- `add_face(name: str) -> bool`

  인물 얼굴을 데이터 베이스에 추가하는 서비스.

- `delete_face(name: str) -> bool`

  특정 인물을 데이터 베이스에서 삭제하는 서비스.

- `face_recognition(timeout: double) -> str`

  timeout 시간동안 얼굴을 검출하여 어떤 인물인지 판단하는 서비스. 만약 timeout 시간 동안 얼굴이 검출되지 않는 경우 `None`을 반환한다.

- `face_recognition_from_file(img_path: str, timeout: double) -> str`

  특정 이미지 파일로 부터 인물을 추출하는 서비스.

## Value Services

- (없음)
