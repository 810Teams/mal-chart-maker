"""
    `classes/user.py`
"""

from src.classes.info import Info
from src.classes.list import List


class User:
    """ User class """
    def __init__(self, info: Info, anime_list: List, manga_list: List):
        """ Constructor """
        self.info = info
        self.anime_list = anime_list
        self.manga_list = manga_list
