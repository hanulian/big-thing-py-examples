# 설명

네이버의 클라우드 서비스를 제공하는 Thing 예제

# 사전 준비

1. [네이버 API 설정](https://www.notion.so/API-1e2fb13ddc09427394cbe6de051afd6b)
2. [secret.py](http://secret.py) 를 생성하여 자신의 API_KEY, 를 설정

   ```python
   API_KEY = '****'
   CLIENT_ID = '****'
   ```

# 실행

```bash
cd big_thing/TTS_big_thing
pip install -r requirements.txt
python run.py
```

# 옵션

- `-n, --name | default = None`
  Thing의 이름. 이 이름은 Thing을 구분하기 위한 ID이기도 하다
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

- `face_detect(image: str) -> bool`
  이미지 경로를 입력으로 받아 얼굴을 인식하는 기능을 제공하는 서비스.
- `face_detect_celebrity(image: str) -> bool`
  이미지 경로를 입력으로 받아 연예인 얼글 닮은꼴 기능을 인식하는 기능을 제공하는 서비스.
- `papago(text: str, src: str, dst: str) -> bool`
  text를 입력으로 받아 목표 언어로 번역 기능을 제공하는 서비스.
- `papago_detect_lang(image: str) -> bool`
  text를 입력으로 받아 언어 인식 기능을 제공하는 서비스.

## Value Services

- (없음)
