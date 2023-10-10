from big_thing_py.utils.log_util import *
from big_thing_py.utils.exception_util import *

from youtubesearchpython import VideosSearch
from pytube import YouTube

# from urllib.parse import urlparse


def get_youtube(keyword: str) -> Union[str, bool]:
    url_list = search_youtube(keyword)
    for url in url_list:
        target_url = _get_youtube(url)
        if not target_url:
            continue
        return target_url
    else:
        return False


def _get_youtube(url: str) -> Union[str, bool]:
    try:
        yt = YouTube(url)
        if not bool(
            url.startswith('https://')
            or url.startswith('http://')
            or url.startswith('youtu.be')
            or url.startswith('youtube.com')
        ):
            print('not youtube url...')
            return False

        target_url = yt.streams.filter(only_audio=True).last()
        # info = dict(
        #     webpage_url=url,
        #     title=yt.title,
        #     uploader=yt.author,
        #     uploader_url=yt.channel_url,
        #     target_url=target_url.url,
        #     thumbnail=yt.thumbnail_url,
        # )
        return target_url.url
    except Exception as e:
        print_error(e)
        return False


def search_youtube(query: str, max_results=5) -> List[str]:
    try:
        videos_search = VideosSearch(query, limit=max_results)

        if videos_search.result()['result']:
            video_info_list = videos_search.result()['result']
            video_url_list = [video_info['link'] for video_info in video_info_list]
            return video_url_list
        else:
            MXLOG_DEBUG(f'No video found for {query}', 'red')
            return False
    except Exception as e:
        print(f'오류 발생: {e}')
        return False


# def is_valid_url(input_string) -> bool:
#     try:
#         result = urlparse(input_string)
#         return all([result.scheme, result.netloc])
#     except ValueError:
#         return False


if __name__ == '__main__':
    START_LOGGER()
    res = get_youtube('화날 때 듣는 노래')
    print(res['target_url'])
