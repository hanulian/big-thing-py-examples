from big_thing_py.utils.log_util import *
from big_thing_py.utils.exception_util import *

from yt_dlp import YoutubeDL


YDL_OPTS = {
    'quiet': True,
    'extract_flat': True,
    'force_generic_extractor': True,
}


def get_youtube(keyword: str) -> Union[str, bool]:
    url_list = search_youtube(keyword)
    for url in url_list:
        target_url = _get_youtube(url)
        if not target_url:
            continue
        return target_url
    else:
        return False


def _get_youtube(url: str, mode: str = 'file') -> Union[str, bool]:
    try:
        if not bool(
            url.startswith('https://')
            or url.startswith('http://')
            or url.startswith('youtu.be')
            or url.startswith('youtube.com')
        ):
            print('not youtube url...')
            return False

        ydl_opts = YDL_OPTS.copy()
        ydl_opts.update(
            {
                'format': 'bestaudio',
                # 'outtmpl': 'download_%(title)s.%(ext)s',
                'outtmpl': 'downloaded_music.%(ext)s',
            }
        )
        audio_downloader = YoutubeDL(ydl_opts)
        if mode == 'url':
            result = audio_downloader.extract_info(url, download=False)
            return result['url']
        elif mode == 'file':
            result = audio_downloader.extract_info(url, download=True)
            return result['requested_downloads'][0]['filepath']
    except Exception as e:
        print_error(e)
        return False


def search_youtube(key_word: str, max_results=5) -> List[str]:
    try:
        with YoutubeDL(YDL_OPTS) as ydl:
            result = ydl.extract_info(f"ytsearch{max_results}:{key_word}", download=False)
            return [result['url'] for result in result['entries'] if result['ie_key'] == 'Youtube']
    except Exception as e:
        print(f'오류 발생: {e}')
        return False


if __name__ == '__main__':
    START_LOGGER()
    # res = get_youtube('화날 때 듣는 노래')
    search_result = search_youtube('화날 때 듣는 노래')
    for url in search_result:
        stream_url_result = _get_youtube(url, mode='file')
        print(f'stream_url_result: {stream_url_result}')
