from samples.big_thing.google_api_big_thing.google_api_utils import GoogleAPIClient

if __name__ == '__main__':
    google_api_client = GoogleAPIClient()
    google_api_client.detect_face('img/angry_sample.jpg')
