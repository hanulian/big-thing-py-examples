# 설명

카메라 캡쳐기능을 제공하는 Thing 예제

# 의존성

```bash
pip install picamera
sudo raspi-config # Interface Options -> Legacy Camera -> Yes -> Ok -> Esc(quit)
sudo reboot
```

# 실행

```bash
cd big_thing/camera_big_thing
pip install -r requirements.txt
python run.py [options]
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

- `capture(file_name: str) -> bool`
    
    카메라로 영상을 캡쳐하여 file_name의 이름으로 저장하는 서비스. 성공하는 경우 True를 반환한다. 
    

## Value Services

- (없음)