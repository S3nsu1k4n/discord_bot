import requests
import json
session = requests.session()
session.trust_env = False
api_url = 'https://reddit-meme-api.herokuapp.com/'

params = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}


def get_reddit_meme() -> dict:
    response = session.get(url=api_url, params=params)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        content_json = json.loads(content)
        return content_json


if __name__ == '__main__':
    print(get_reddit_meme())
