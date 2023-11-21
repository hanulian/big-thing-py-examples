import time
import platform
import subprocess
import requests
from typing import Union

from big_thing_py.utils import *

try:
    import vlc
except ImportError as e:
    if platform.uname().system == 'Windows':
        subprocess.check_call("winget install VideoLAN.VLC", shell=True)
    elif platform.uname().system == 'Darwin':
        subprocess.check_call("brew install vlc", shell=True)
    elif platform.uname().system == 'Linux':
        subprocess.check_call("sudo apt install vlc -y", shell=True)

    import vlc


class VLCPlayer:
    def __init__(self) -> None:
        self._vlc_instance = vlc.Instance()
        self._player: vlc.MediaPlayer = self._vlc_instance.media_player_new()
        self._player.event_manager().event_attach(
            vlc.EventType.MediaPlayerPositionChanged, self._update_playback_percentage
        )

    def _update_playback_percentage(self, event):
        if event.type == vlc.EventType.MediaPlayerPositionChanged:
            current_time = self._player.get_time()
            total_length = self._player.get_length()
            if total_length:
                playback_percentage = (current_time / total_length) * 100
            else:
                playback_percentage = 0

            print(f"\r재생 중: {playback_percentage:.2f}%", end='')

    def is_playing(self) -> bool:
        return self._player.is_playing()

    def play(self, source: str, block: bool = False):
        media = self._vlc_instance.media_new(source)
        self._player.set_media(media)

        self._player.play()
        if block:
            while not self._player.is_playing():
                time.sleep(THREAD_TIME_OUT)
            while self._player.is_playing():
                time.sleep(0.1)

    def pause_toggle(self):
        self._player.pause()

    def stop(self):
        self._player.stop()


def download_file(url: str) -> Union[str, bool]:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        file_name = url.split('/')[-1]

        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"파일 다운로드 완료: {file_name}")
        return file_name
    except Exception as e:
        print(f"파일 다운로드 중 오류 발생: {e}")
        return False


if __name__ == '__main__':
    sample_audio_file_url = (
        'https://file-examples.com/storage/feaade38c1651bd01984236/2017/11/file_example_MP3_700KB.mp3'
    )
    # sample_audio_file_url = 'https://file-examples.com/storage/feaade38c1651bd01984236/2017/11/file_example_WAV_1MG.wav'
    local_file = os.path.basename(sample_audio_file_url)
    vlc_player = VLCPlayer()

    if not os.path.exists(local_file):
        local_file = download_file(sample_audio_file_url)

    if local_file:
        vlc_player.play(local_file, block=True)
    else:
        print("파일 다운로드 실패")
