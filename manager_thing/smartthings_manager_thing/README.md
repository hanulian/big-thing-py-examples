# 예제 설명

삼성 스마트씽스 써드파티 디바이스를 통제할 수 있는 Thing 예제

# 사전 준비

## 스마트씽스 앱 준비

<aside>
💡 스마트씽스 디바이스는 Wi-Fi를 사용하는 디바이스를 가정하고 있습니다.

따라서 브릿지나 허브같은 제품군이 존재하지 않습니다.

</aside>

1. 스마트씽스 앱에서 + 버튼을 눌러 기기를 스캔합니다. 
2. 검색된 디바이스를 앱의 지시에 따라 등록 완료합니다. 
3. [링크](https://account.smartthings.com/tokens)에서 스마트씽스 API 키를 받습니다. 
4. [SmartThingsAPI 문서](https://developer-preview.smartthings.com/docs/api/public)를 참고 하여 커스텀 SmartThings Manager Thing을 제작한다. **(*Advanced*)**

# 실행

```bash
cd manager_thing/smartthings_manager_thing
python run.py [options]
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
    
- `-bip, --bridge_host | default='https://api.smartthings.com/v1/'`
    
    SmartThings 클라우드 브릿지 ip 주소
    
- `-bp, --bridge_port | default=80`
    
    SmartThings 클라우드 브릿지 port 번호
    
- `-k --user_key | default=''`
    
    사용자 API 키
    
- `-sc --scan_cycle | default=60`
    
    SmartThings 디바이스 스캔 주기
    

# Services

## Function Services

- `on(None) -> bool`
    
    SmartThings 디바이스를 켜는 서비스
    
- `off(None) -> bool`
    
    SmartThings 디바이스를 끄는 서비스
    
- `set_brightness(None) -> bool`
    
    SmartThings 디바이스의 밝기를 조정하는 서비스
    

## Value Services

- (없음)