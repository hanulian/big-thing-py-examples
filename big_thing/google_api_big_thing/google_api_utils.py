from big_thing_py.utils.log_util import *
from big_thing_py.utils.exception_util import *

from google.cloud import vision
from pytube import YouTube
from youtube_utils import get_youtube


class GoogleAPIClient:
    VISION_API_ENDPOINT = 'https://vision.googleapis.com/v1/images:annotate'
    LIKELIHOOD_NAME = (
        'UNKNOWN',
        'VERY_UNLIKELY',
        'UNLIKE',
        'POSSIBLE',
        'LIKELY',
        'VERY_LIKELY',
    )
    SCORE_MAP = [
        'UNKNOWN',
        'VERY_UNLIKELY',
        'UNLIKE',
        'POSSIBLE',
        'LIKELY',
        'VERY_LIKELY',
    ]
    KEYWORD_MAP = {
        'anger': '짜증',
        'joy': '기쁨',
        'sorrow': '슬픔',
    }

    def __init__(self, client_id: str = None, api_key: str = None) -> None:
        self._vision_api_client: vision.ImageAnnotatorClient = None

        self._client_id = client_id
        self._api_key = api_key
        self._headers = {}

    def _load_image(self, image_path: str) -> bytes:
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        return content

    def _emotion_classification(self, face) -> List[str]:
        emotion_scores = {
            'anger': int(face.anger_likelihood),
            'joy': int(face.joy_likelihood),
            'sorrow': int(face.sorrow_likelihood),
            # 'surprise': int(face.surprise_likelihood),
            # 'blurred': int(face.blurred_likelihood),
            # 'headwear': int(face.headwear_likelihood),
            # 'under_exposed': int(face.under_exposed_likelihood),
        }

        max_score = max(emotion_scores.values())
        max_emotions = [emotion for emotion, score in emotion_scores.items() if score == max_score]

        confidence = face.detection_confidence
        vertices = [f'({vertex.x}, {vertex.y})' for vertex in face.bounding_poly.vertices]

        return max_emotions

    def detect_face(self, image_path: str) -> str:
        try:
            if not self._vision_api_client:
                self._vision_api_client = vision.ImageAnnotatorClient()

            content = self._load_image(image_path)
            image = vision.Image(content=content)
            response = self._vision_api_client.face_detection(image=image)
            faces = response.face_annotations

            if response.error.message:
                error_msg = (
                    f'{response.error.message}\nFor more info on error messages, check: '
                    f'https://cloud.google.com/apis/design/errors'
                )
                raise Exception(error_msg)
            elif len(faces) == 0:
                return 'no face'
            elif len(faces) > 1:
                return 'too many faces'
            else:
                emotion_state = self._emotion_classification(faces[0])

            MXLOG_DEBUG(f'emotion state: {emotion_state}')
            return ', '.join(emotion_state)
        except Exception as e:
            print_error(e)
            return error_msg

    def recommend_song(self, emotion_state: str) -> str:
        emotion_list = emotion_state.split(', ')
        keyword = (
            ' '.join([self.KEYWORD_MAP[emotion] for emotion in emotion_list if emotion in self.KEYWORD_MAP.keys()])
            + ' 때 노래'
        )
        target_url = get_youtube(keyword)
        return target_url


if __name__ == '__main__':
    START_LOGGER()
    client = GoogleAPIClient()
    emotion_state = client.detect_face('./joy.jpg')
    target_url = client.recommend_song(emotion_state)
    print(target_url)
