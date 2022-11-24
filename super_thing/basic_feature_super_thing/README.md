# 설명

SoPIoT 시스템에서 Super Thing의 기본적인 기능을 테스트 해볼 수 있는 예제 
([기본 Thing](https://www.notion.so/Thing-3211d2394d72472bab238b0b004ee6bc)과 같이 작동)

# 실행

```bash
cd super_thing/basic_feature_super_thing
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
    
- `-rc, --refresh_cycle | default=5`
    
    Thing의 refresh 패킷 전송 주기. refresh 패킷을 Middleware가 감지하면 MS/SERVICE_LIST 패킷을 Super Thing에게 보내준다. Super Thing은 해당 패킷을 받아 현재 Middleware Tree내의 Service리스트를 파악한다. 
    
- `--log | default=True`
    
    Thing의 log기능의 활성화 여부. 
    

# Services

## Function Services

- `super_func_execute_func_no_arg_SINGLE(None) -> int`
    
    하위 레벨에 있는 `basic_big_thing`의 `func_no_arg`서비스를 램덤으로 하나 호출하는 슈퍼 서비스
    
- `super_func_execute_func_no_arg_ALL(None) -> int`
    
    하위 레벨에 있는 `basic_big_thing`의 `func_no_arg`서비스를 모두 호출하는 슈퍼 서비스
    
- `super_func_get_value_current_time_SINGLE(None) -> int`
    
    하위 레벨에 있는 `basic_big_thing`의 `current_time` 서비스를 램덤으로 하나 호출하는 슈퍼 서비스
    
- `super_func_get_value_current_time_ALL(None) -> int`
    
    하위 레벨에 있는 `basic_big_thing`의 `current_time` 서비스를 모두 호출하는 슈퍼 서비스
    

## Value Services

- (없음)