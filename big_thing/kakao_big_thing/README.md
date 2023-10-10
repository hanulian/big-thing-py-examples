# 설명

카카오의 클라우드 서비스를 제공하는 Thing 예제

# 사전 준비

1. [카카오 API 설정](https://www.notion.so/API-de912721240a40cf97bfcd7e3b6c74f4)
2. [secret.py](http://secret.py) 를 생성하여 자신의 API_KEY를 설정

   ```python
   API_KEY = '****'
   ```

# 실행

```bash
cd big_thing/kakao_big_thing
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

- `search(text: str) -> bool`
  text를 입력으로 받아 다음 사이트에서 검색 기능을 제공하는 서비스
- `pose(image: str) -> bool`
  사람 이미지 경로 또는 url을 입력으로 받아 포즈 인식 기능을 제공하는 서비스
- `OCR(text: str) -> bool`
  글자 이미지 경로를 입력으로 받아 OCR 기능을 제공하는 서비스
- `translation(text: str, src: str, dst: str) -> bool`
  text를 입력으로 받아 목표 언어로 번역하는 기능을 제공하는 서비스

## Value Services

- (없음)
