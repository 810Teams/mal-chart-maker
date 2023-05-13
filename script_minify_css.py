"""
    minify_css.py
"""

from settings import CSS_NAME, CSS_PATH, MIN_CSS_PATH
from src.utils import notice

import platform
import requests


def main():
    data = {'input': open(CSS_PATH, 'rb').read()}
    response = requests.post('https://cssminifier.com/raw', data=data)

    min_data = open(MIN_CSS_PATH, 'w')
    min_data.write(response.text)
    min_data.close()

    print()
    notice('Minified CSS `{}` has been created, minified from {} to {} characters.'.format(
        CSS_NAME,
        len(''.join(list(open(CSS_PATH)))),
        len(response.text)
    ))

    # Windows' cmd fix
    if platform.system() != 'Windows':
        print()


main()
