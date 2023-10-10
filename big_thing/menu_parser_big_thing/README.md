# 설명

서울대 학식 메뉴 알리미 서비스를 제공하는 Thing 예제.

# 의존성

```bash
pip install -r requirements.txt
```

# 실행

```bash
cd big_thing/menu_parser_big_thing
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

- `menu(command: str) -> str`

  서울대 학식 메뉴 정보를 제공하는 서비스. command는 다음과 같이 작성할 수 있습니다.

  ```bash
  오늘 301동 점심
  오늘 자하연 저녁
  내일 기숙사식당 아침

  format:
  [오늘|내일] [학생식당|수의대식당|전망대(3식당)|예술계식당(아름드리)|기숙사식당|아워홈|동원관식당(113동)|웰스토리(220동)|투굿(공대간이식당)|자하연식당|301동식당] [아침|점심|저녁]
  ```

## Value Services

- (없음)
