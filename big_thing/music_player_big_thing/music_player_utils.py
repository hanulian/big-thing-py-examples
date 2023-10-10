import vlc


class VLCPlayer:
    def __init__(self) -> None:
        self._vlc_instance = vlc.Instance()
        self._player: vlc.MediaPlayer = self._vlc_instance.media_player_new()

    def play(self, source: str):
        media = self._vlc_instance.media_new(source)
        self._player.set_media(media)
        self._player.play()

    def pause_toggle(self):
        self._player.pause()

    def stop(self):
        self._player.stop()
