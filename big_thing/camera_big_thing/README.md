# 설명

카메라 캡쳐기능을 제공하는 Thing 예제.

# 의존성

- Windows

  1. 필요한 python 모듈 설치.

     ```bash
     pip install -r requirements.txt
     ```

- Mac

  1. 필요한 python 모듈 설치.

     ```bash
     pip install -r requirements.txt
     ```

  2. 앱 실행시 다음과 같이 권한 부여 팝업이 뜹니다. 이 때 확인을 눌러 카메라 권한을 부여합니다. (**_반드시 맥 GUI 환경에서 실행하여야 다음과 같은 팝업이 뜨니 원격접속대신 직접 맥북을 사용하시기 바랍니다._**)

     ![Untitled](img/mac_permission.png)

- Raspberry Pi

  1. 필요한 라이브러리, python 모듈 설치.

     ```bash
     sudo apt install libatlas-base-dev python3-dev -y
     pip install -r requirements.txt
     ```

## 카메라 설치

- Raspberry Pi

  1. 아래와 같은 Raspberry Pi용 카메로 모듈 준비.

     ![Untitled](img/raspi_cam.jpeg)

  2. Raspberry Pi와 결합.

     ![Untitled](img/attach_cam.png)

- 그 외 플랫폼

  1. 웹캠 준비.

     ![Untitled](img/webcam.png)

  2. 노트북의 경우 내장된 웹캠 사용 가능.

     ![Untitled](img/laptop_webcam.png)

# 실행

```bash
cd big_thing/camera_big_thing
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

- `capture() -> str`

  카메라로 영상을 캡쳐하여 저장하는 서비스. 성공하는 경우 이미지가 저장된 절대 경로를 반환한다. 이미지의 이름은 `현재_시간.jpg`로 저장됩니다.

- `capture_with_filename(file_name: str) -> str`

  카메라로 영상을 캡쳐하여 file_name의 이름으로 저장하는 서비스. 성공하는 경우 이미지가 저장된 절대 경로를 반환한다.

## Value Services

- (없음)
