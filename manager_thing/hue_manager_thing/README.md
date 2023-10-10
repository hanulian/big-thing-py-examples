# 예제 설명

필립스 휴 써드파티 디바이스를 통제할 수 있는 Thing 예제.

# 사전 준비

## 휴 브릿지 준비

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d2d7085c-9ebb-4ce5-8dc5-a6ddd5aeb91e/Untitled.png)

필립스 휴 시스템을 구축하기 위해서는 Hue Bridge가 필요합니다.

1. [링크](https://ko.manuals.plus/philips/929001180603-hue-smart-bridge-manual)를통해 필립스 휴 브릿지를 온라인 상태로 셋팅합니다.
2. 휴 앱으로 휴 디바이스를 휴 브릿지에 연결합니다.
3. [링크](https://developers.meethue.com/develop/get-started-2/)에서 개발자 등록.
4. `http://{브릿지_ip}/debug/clip.html` 로 접속하여 **CLIP API Debugger**를 띄운다.
5. 휴 브릿지 버튼을 누른 후 다음의 셋팅으로 사용자 API 키를 받아온다.

   **URL**: `api/`

   **body**: `{"devicetype":"my_hue_app#iphone peter"}`

   **Method**: `POST`

6. [Hue API 문서](https://developers.meethue.com/develop/hue-api-v2/api-reference/)를 참고 하여 커스텀 Hue Manager Thing을 제작한다. **(_Advanced_)**

# 실행

```bash
cd manager_thing/hue_manager_thing
python run.py
```

# 옵션

- `-n, --name | default = None`

  Thing의 이름. 이 이름은 Thing을 구분하기위한 ID이기도 하다.

- `-ip --host | default='127.0.0.1'`

  Thing의 ip 주소.

- `-p, --port | default=1883`

  Thing의 port 번호.

- `-ac, --alive_cycle | default=60`

  Thing의 alive 패킷 전송 주기. alive 패킷을 통해 Middleware가 Thing의 활성화 여부를 파악한다.

- `-as, --auto_scan | default=True`

  Middleware 자동스캔 기능 활성화 여부.

- `-bip, --bridge_host | default='https://goqual.io/openapi'`

  Hue 브릿지 ip 주소.

- `-bp, --bridge_port | default=80`

  Hue 브릿지 port 번호.

- `-k --user_key | default=''`

  사용자 API 키.

- `-sc --scan_cycle | default=60`

  Hue 디바이스 스캔 주기.

- `-md --mode | default=MXManagerMode.SPLIT.value`

  Manager Thing 모드.

  1. `MXManagerMode.SPLIT`

     Hue 디바이스가 별개의 Thing으로써 동작.

  2. `MXManagerMode.JOIN`

     Hue 디바이스가 한 개의 Thing으로 묶여서 동작.

# Services

## Function Services

- `on(None) -> bool`

  Hue 디바이스를 켜는 서비스.

- `off(None) -> bool`

  Hue 디바이스를 끄는 서비스.

- `set_brightness(brightness: int) -> bool`

  Hue 디바이스의 밝기를 조정하는 서비스.

- `set_color(r: int, g: int, b: int) -> bool`

  Hue 디바이스의 색을 조정하는 서비스.

- `set_brightness(brightness: int) -> bool`

  Hue 디바이스의 밝기를 조정하는 서비스.

- `set_brightness(brightness: int) -> bool`

  Hue 디바이스의 밝기를 조정하는 서비스.

## Value Services

- (없음)
