# 예제 설명

헤이홈 써드파티 디바이스를 통제할 수 있는 Thing 예제.

# 사전 준비

## 헤이홈 스마트 허브 Air 준비

![a4fa1b48aaab8.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/81dea08f-b965-45c3-932a-d72294849763/a4fa1b48aaab8.jpg)

<aside>
💡 헤이홈 디바이스는 **Wi-Fi를 사용하는 디바이스**와 **Zigbee를 이용하는 디바이스** 2가지 종류가 있습니다.

Wi-Fi 제품의 경우 Wi-Fi 공유기만 갖추면 되지만 Zigbee 제품의 경우 **헤이홈 스마트 허브**가 필요합니다.

</aside>

1. 헤이홈 앱에서 자동스캔 기능을 이용하여 디바이스를 검색합니다.
2. 검색된 디바이스를 앱의 지시에 따라 등록 완료합니다.
3. 조교에 문의하여 헤이홈 API 키를 받습니다.
4. [고퀄 API 문서](https://documenter.getpostman.com/view/7113846/SW14WHx6)를 참고 하여 커스텀 Hejhome Manager Thing을 제작한다. **(_Advanced_)**

# 실행

```bash
cd manager_thing/hejhome_manager_thing
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

  Hejhome 클라우드 브릿지 ip 주소.

- `-bp, --bridge_port | default=80`

  Hejhome 클라우드 브릿지 port 번호.

- `-k --user_key | default=''`

  사용자 API 키.

- `-sc --scan_cycle | default=60`

  Hejhome 디바이스 스캔 주기.

# Services

## Function Services

- `on(None) -> bool`

  Hejhome 디바이스를 켜는 서비스.

- `off(None) -> bool`

  Hejhome 디바이스를 끄는 서비스.

- `curtain_open(None) -> bool`

  커튼 Hejhome 디바이스의 커튼을 여는 서비스.

- `curtain_close(None) -> bool`

  커튼 Hejhome 디바이스의 커튼을 는 서비스.

- `switch_set(index: int, on: bool) -> bool`

  zigbee Hejhome 스위치 디바이스의 전원을 조정하는 서비스.

## Value Services

- (없음)
