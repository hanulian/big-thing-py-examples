from google_api_utils import GoogleAPIClient

if __name__ == '__main__':
    google_api_client = GoogleAPIClient()
    google_api_client.detect_emotion('img/angry_sample.jpg')
