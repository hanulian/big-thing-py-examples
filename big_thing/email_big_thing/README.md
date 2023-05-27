# 설명

이메일 전송 기능을 제공하는 Thing 예제

# 의존성

- gmail
    1. https://myaccount.google.com/security 에 접속하여 **2단계 인증**을 클릭하여 **앱 비밀번호**를 설정 
    2. 기타를 선택하여 앱 비밀번호 생성
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3f7f751c-daa7-49e0-a88b-171e92b4fc6b/Untitled.png)
        
    3. 생성된 앱 비밀번호를 복사 또는 저장해두기
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/68799485-7a0a-4f3d-9a4b-d420ed993162/Untitled.png)
        
    4. 생성된 앱 비밀번호를 [secret.py](http://secret.py/) 파일의 `EMAIL_PASSWORD_GMAIL`의 값으로 설정
    5. [run.py](http://run.py/)의 `SENDER_EMAIL`을 자신의 gmail 주소로 설정

# 실행

```bash
cd big_thing/email_big_thing
python run.py
```

# 옵션

- `-n, --name | default = None`
    
    Thing의 이름. 이 이름은 Thing을 구분하기 위한 ID이기도 하다 
    
- `-ip --host | default='127.0.0.1'`
    
    Thing의 ip 주소
    
- `-p, --port | default=11083`
    
    Thing의 port 번호
    
- `-ac, --alive_cycle | default=60`
    
    Thing의 alive 패킷 전송 주기. alive 패킷을 통해 Middleware가 Thing의 활성화 여부를 파악한다. 
    
- `-as, --auto_scan | default=True`
    
    Middleware 자동스캔 기능 활성화 여부.
    
- `--log | default=True`
    
    Thing의 log기능의 활성화 여부. 
    

# Services

## Function Services

- `send(receive_address:str, title:str, text: str, attachment_path: str) -> bool`
    
    `title`의 제목을 가지고 `text`입 의 본문을 가지는 이메일을 `receive_address`로 전송하는 서비스. 
    
- `send_with_file(receive_address:str, title:str, text: str, attachment_path: str) -> bool`
    
    `send`의 서비스의 기능에 첨부파일 첨부기능을 추가한 서비스.
    

## Value Services

- (없음)