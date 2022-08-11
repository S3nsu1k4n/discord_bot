import requests
import json
from random import choice
session = requests.session()
session.trust_env = False

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'de-DE,de;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

subreddits = [
    'dankmemes',
    'memes',
    'AdviceAnimals',
    'MemeEconomy',
    'me_irl',
    'ComedyCemetery',
    'terriblefacebookmemes',
    'OkBrudiMongo',
    'wasletztepreis',
    'amthor',
    'LindnerWichsvorlagen',
    'classicalartmemes',
    'Animemes',
    'animememes',
    'PoliticalCompassMemes',
    #'okbuddyretard',
    'trippinthroughtime',
    'marvelmemes',
    'im14andthisisdeep',
    'amthorwichsvorlagen',
    'ich_iel',
    'kidsarefuckingstupid',
    'MemePiece',
    #'GoodAnimemes',
    'raimimemes',
    'funny',
    'wholesomememes',
    'suicidebywords',
    #'HistoryMemes',
]


def get_api_response(url: str, is_json=False) -> dict:
    response = session.get(url=url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        if is_json:
            return json.loads(content)
        return content
    return {}


def get_posted_timestamp(url: str) -> str:
    try:
        data = get_api_response(url)
        data = data[data.find('Gepostet von'):]
        data = data[:data.find('</span></div>')]
        return data[data.rfind('>')+1:]
    except Exception:
        return ''


def get_reddit_meme() -> dict:
    topic = choice(subreddits)
    api_url = 'https://reddit-meme-api.herokuapp.com/' + topic + '/1'
    response = get_api_response(url=api_url, is_json=True)
    response.update({'timestamp': get_posted_timestamp(url=response['post_link'])})

    if response['url'].find('v.redd.it') != -1:
        fallback_json = response['post_link'].replace('redd.it', 'reddit.com') + '.json'
        fallback_resp = get_api_response(fallback_json, is_json=True)
        response['url'] = fallback_resp[0]['data']['children'][0]['data']['media']['reddit_video']['fallback_url']

    return response


def get_cat_api_image_url() -> dict:
    api_url = 'https://api.thecatapi.com/v1/images/search?format=json'
    return get_api_response(url=api_url, is_json=True)[0]


if __name__ == '__main__':
    print(get_cat_api_image_url())
