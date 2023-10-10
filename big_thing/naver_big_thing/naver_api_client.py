from big_thing_py.utils import *


class NaverAPIClient:
    def __init__(self, client_id: str = None, api_key: str = None) -> None:
        self.client_id = client_id
        self.api_key = api_key
        self.headers = {"X-Naver-Client-Id": self.client_id, "X-Naver-Client-Secret": self.api_key}

    # def search(self, ):
    #     url = "https://openapi.naver.com/v1/datalab/search"
    #     self.headers['Content-Type'] = 'application/json'

    #     files = "{\"startDate\":\"2017-01-01\",\"endDate\":\"2017-04-30\",\"timeUnit\":\"month\",\"keywordGroups\":[{\"groupName\":\"한글\",\"keywords\":[\"한글\",\"korean\"]},{\"groupName\":\"영어\",\"keywords\":[\"영어\",\"english\"]}],\"device\":\"pc\",\"ages\":[\"1\",\"2\"],\"gender\":\"f\"}"

    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id", self.client_id)
    #     request.add_header("X-Naver-Client-Secret", self.api_key)
    #     request.add_header("Content-Type", "application/json")
    #     response = urllib.request.urlopen(request, data=files.encode("utf-8"))
    #     rescode = response.getcode()
    #     if (rescode == 200):
    #         response_body = response.read()
    #         print(response_body.decode('utf-8'))
    #     else:
    #         print("Error Code:" + rescode)

    def face_detect(self, image: str):
        url = "https://openapi.naver.com/v1/vision/face"  # 얼굴감지

        files = {'image': open(image, 'rb')}
        response = requests.post(url, files=files, headers=self.headers)
        rescode = response.status_code
        if rescode == 200:
            return response.text
        else:
            return f"Error Code: {rescode}"

    def face_detect_celebrity(self, image: str) -> str:
        url = "https://openapi.naver.com/v1/vision/celebrity"  # 유명인 얼굴인식

        files = {'image': open(image, 'rb')}
        response = requests.post(url, files=files, headers=self.headers)
        rescode = response.status_code
        if rescode == 200:
            return json_string_to_dict(response.text)['faces'][0]['celebrity']['value']
        else:
            return "해당없음"

    def papago(self, text: str, src: str, dst: str):
        url = "https://openapi.naver.com/v1/papago/n2mt"

        data = {'source': src, 'target': dst, 'text': text.encode('utf-8')}

        response = requests.post(url, data=data, headers=self.headers)
        rescode = response.status_code

        if rescode == 200:
            return json_string_to_dict(response.text)['message']['result']['translatedText']
        else:
            return f"Error Code: {rescode}"

    def papago_detect_lang(self, text: str):
        url = "https://openapi.naver.com/v1/papago/detectLangs"

        data = {'query': text.encode('utf-8')}

        response = requests.post(url, data=data, headers=self.headers)
        rescode = response.status_code

        if rescode == 200:
            return response.text
        else:
            return f"Error Code: {rescode}"
