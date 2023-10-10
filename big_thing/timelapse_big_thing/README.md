# 설명

일정시간마다 사진을 찍어 타임랩스 동영상을 만들 수 있는 Thing 예제.

# 의존성

[의존성 및 카메라 모듈 설치](../camera_big_thing/README.md) 참고.

# 실행

```bash
cd big_thing/timelapse_big_thing
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

- `--log | default=True`

  Thing의 log기능의 활성화 여부.

# Services

## Function Services

- `timelapse_start(None) -> int`

  타입랩스 캡쳐를 시작하는 서비스.

- `timelapse_stop(None) -> int`

  타입랩스 캡쳐를 중지하는 서비스.

- `make_video(video_dst_path: str) -> int`

  캡쳐한 사진을 비디오로 변환하는 서비스. 변환에 성공하면 True를 반환한다.
  캡쳐한 이미지들은 기본적으로 `./capture_images` 에 저장되고, 변환된 동영상은 `video_dst_path`에 명세된 경로 에 저장됩니다.

## Value Services

- (없음)
