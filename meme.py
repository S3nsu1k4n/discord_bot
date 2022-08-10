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
        """ {
                'code': 200,
                'post_link': 'https://redd.it/whq5l7',
                'subreddit': 'ComedyCemetery',
                'title': '“Uncultured”',
                'url': 'https://i.redd.it/wmpxuzotw3g91.jpg',
                'ups': 32,
                'author': 'stnick6',
                'spoilers_enabled': True,
                'nsfw': False,
                'image_previews': ['https://preview.redd.it/wmpxuzotw3g91.jpg?width=108&crop=smart&auto=webp&s=75f889b89e825b2f47504a5b909604438545d303', 'https://preview.redd.it/wmpxuzotw3g91.jpg?width=216&crop=smart&auto=webp&s=2e1dca9283e7e40f0e2458a83d75af20a0e8380e', 'https://preview.redd.it/wmpxuzotw3g91.jpg?width=320&crop=smart&auto=webp&s=8ae687b12e6aab724f5cb802d89cea77c131ca97', 'https://preview.redd.it/wmpxuzotw3g91.jpg?width=640&crop=smart&auto=webp&s=d1f3dec50d999e0839f5de2609e20b45852b6344', 'https://preview.redd.it/wmpxuzotw3g91.jpg?width=960&crop=smart&auto=webp&s=d5d6be8f8c55a57e784a7932333ed03c5730b3f7']}
                """
        return content_json


if __name__ == '__main__':
    print(get_reddit_meme())