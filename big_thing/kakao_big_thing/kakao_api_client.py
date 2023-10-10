from big_thing_py.utils import *
from kakaotrans import Translator


class KakaoAPIClient:
    def __init__(self, api_key: str = None) -> None:
        self.api_key = api_key
        self.headers = {'Authorization': f'KakaoAK {self.api_key}'}

    def search(self, text) -> dict:
        '''
        Ref: https://developers.kakao.com/docs/latest/ko/daum-search/dev-guide
        '''
        url = 'https://dapi.kakao.com/v2/search/web'
        params = {'query': text}
        data = None
        response = requests.get(url, headers=self.headers, params=params, data=data)
        return response.json()

    def pose(self, image: str) -> dict:
        '''
        Ref: https://developers.kakao.com/docs/latest/ko/pose/dev-guide
        '''

        url = "https://cv-api.kakaobrain.com/pose"
        params = None
        data = {'image_url': image} if 'http' in image else None
        files = {'file': open(image, 'rb').read()} if 'http' not in image else None
        response = requests.post(url=url, headers=self.headers, params=params, data=data, files=files)
        return response.json()

    def OCR(self, image: str):
        '''
        Ref: https://www.kakaoicloud.com/service/detail/6-9
        '''
        url = "https://dapi.kakao.com/v2/vision/text/ocr"
        params = None
        data = None
        files = {'image': open(image, 'rb').read()} if 'http' not in image else None
        response = requests.post(url=url, headers=self.headers, params=params, data=data, files=files)
        return response.json()

    def translation(self, text: str, src: str, dst: str):
        '''
        Ref: https://www.kakaoicloud.com/service/detail/6-10
        '''
        translator = Translator()
        # result = translator.translate("Try your best rather than be the best.")
        result = translator.translate(text, src, dst)
        return result

        # url = 'https://dapi.kakao.com/v2/translation/translate'
        # params = None
        # data = { 'query': '안녕하세요. 반갑습니다.',}
        # files = {'image': open(image, 'rb').read()
        #          } if 'http' not in image else None
        # response = requests.post(
        #     url=url, headers=self.headers, params=params, data=data, files=files)
        # return response.json()

    # def speech_to_text(self):
    #     '''
    #     Ref: https://www.kakaoicloud.com/service/detail/6-23
    #     '''
    #     from pydub import AudioSegment

    #     url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
    #     headers = {
    #         "Content-Type": "application/octet-stream",
    #         "Transfer-Encoding": "chunked",
    #         "Authorization": "KakaoAK " + self.api_key,
    #     }

    #     src = "transcript.mp3"
    #     dst = "test.wav"

    #     audSeg = AudioSegment.from_mp3(src)
    #     audSeg.export(dst, format="wav")

    #     with open('heykakao.wav', 'rb') as fp:
    #         audio = fp.read()

    #     res = requests.post(url, headers=headers, data=audio)
    #     print(res.text)

    # def text_to_speech(self, text: str):
    #     from playsound import playsound
    #     url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
    #     self.headers["Content-Type"] = "application/xml"

    #     data = f"<speak>{text}</speak>".encode('utf-8')
    #     res = requests.post(url, headers=self.headers, data=data)
    #     file_name = 'test_file.wav'
    #     with open(file_name, 'wb') as f:
    #         f.write(res.content)

    #     playsound(file_name)

    # def NLP(self):
    #     '''
    #     Ref: https://www.kakaoicloud.com/service/detail/6-25
    #     '''

    # def Vision(self, image: str):
    #     '''
    #     Ref: https://www.kakaoicloud.com/service/detail/6-28
    #     '''

    # def Conversion(self):
    #     '''
    #     Ref: https://www.kakaoicloud.com/service/detail/6-29
    #     '''
