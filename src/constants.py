"""
    `constants.py`
"""


XML = 'xml'

ANIMELIST = 'animelist'
MANGALIST = 'mangalist'

ANIME_STATUS_LIST = {1: 'Watching', 2: 'Completed', 3: 'On-Hold', 4: 'Dropped', 6: 'Plan to Watch'}
MANGA_STATUS_LIST = {1: 'Reading', 2: 'Completed', 3: 'On-Hold', 4: 'Dropped', 6: 'Plan to Read'}

API_URL = 'https://myanimelist.net/{}/{}/load.json?status=7&offset={}'
