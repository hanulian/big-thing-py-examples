# 예제 설명

<aside>
💡 우분투에서만 사용가능한 예제입니다.

</aside>

물체를 감지하는 서비스를 제공하는 Thing 예제

# 의존성

```
chmod +x preinstall.sh
./preinstall.sh
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

- `get_obj_info(target_label: str) -> bool`
    
    target_label에 해당하는 물체가 있는지 없는지 알려주는 서비스
    

## Value Services

- (없음)
