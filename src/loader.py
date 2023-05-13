"""
    `loader.py`
"""

from xml.dom import minidom
from xml.dom.minidom import Document

from src.classes.entry import Anime, Manga
from src.classes.list import List
from src.classes.info import Info
from src.classes.user import User
from src.constants import XML, API_URL, ANIMELIST, MANGALIST, ANIME_STATUS_LIST, MANGA_STATUS_LIST

import os
import json
import requests


class Loader:
    """ Loader class """
    def __init__(self):
        """ Constructor """
        self.anime_document = None
        self.manga_document = None


class XMLLoader(Loader):
    """ XML Loader class """
    def __init__(self, data_dir: str):
        """ Constructor """
        super().__init__()
        self.data_dir = data_dir

    def fetch_file_name(self, file_format: str=XML, list_type: str=ANIMELIST, target: int=-1):
        """ Fetch file names from the specified directory """
        try:
            return [
                i for i in os.listdir(self.data_dir)
                if i.startswith(list_type) and i.endswith(file_format)
            ][target]
        except IndexError:
            return None

    def create_document(self):
        """ Create document object notation (DOM) object """
        anime_list_file_name = self.fetch_file_name(file_format=XML, list_type=ANIMELIST, target=-1)
        manga_list_file_name = self.fetch_file_name(file_format=XML, list_type=MANGALIST, target=-1)

        self.anime_document = minidom.parse('{}{}'.format(self.data_dir, anime_list_file_name))
        self.manga_document = minidom.parse('{}{}'.format(self.data_dir, manga_list_file_name))

    def get_element(self, document: Document, element_name: str, convert_type: bool=True, get_data: bool=False, get_single: bool=False):
        """ Retrieve elements or data from the specified element name """
        items = document.getElementsByTagName(element_name)

        # Procedure: Retrieve non-element data
        if get_data:
            # Exception Case: Null or composite element data retrieval attempt
            try:
                items = [i.firstChild.data for i in items]

                # Prodecure: Convert type attempt
                if convert_type:
                    try:
                        items = [int(i) for i in items]
                    except ValueError:
                        try:
                            items = [float(i) for i in items]
                        except ValueError:
                            pass
            except AttributeError:
                pass

        # Prodecure: Retrieve a single element or data
        if get_single:
            # Exception Case: Invalid element name
            try:
                items = items[0]
            except IndexError:
                pass

        return items

    def get_user_object(self, include_current: bool=False, include_onhold: bool=False, include_dropped: bool=False, include_planned: bool=False):
        """ Retrieve user object """
        return User(
            info=self.get_info_object(),
            anime_list=self.get_anime_list_object(
                include_current=include_current,
                include_onhold=include_onhold,
                include_dropped=include_dropped,
                include_planned=include_planned
            ),
            manga_list=self.get_manga_list_object(
                include_current=include_current,
                include_onhold=include_onhold,
                include_dropped=include_dropped,
                include_planned=include_planned
            )
        )

    def get_info_object(self):
        """ Retrieve user information object """
        my_info = self.get_element(self.anime_document, 'myinfo', get_single=True)

        return Info(
            user_id=               self.get_element(my_info, 'user_id',                get_data=True, get_single=True),
            user_name=             self.get_element(my_info, 'user_name',              get_data=True, get_single=True),
            user_export_type=      self.get_element(my_info, 'user_export_type',       get_data=True, get_single=True)
        )

    def get_anime_list_object(self, include_current: bool=False, include_onhold: bool=False, include_dropped: bool=False, include_planned: bool=False):
        """ Retrieve user anime list object """
        return List(
            data=[self.get_anime_object(i) for i in self.get_element(self.anime_document, 'anime')],
            include_current=include_current,
            include_onhold=include_onhold,
            include_dropped=include_dropped,
            include_planned=include_planned
        )

    def get_anime_object(self, anime_element: Document):
        """ Retrieve anime object """
        return Anime(
            series_animedb_id=  self.get_element(anime_element, 'series_animedb_id',   get_data=True, get_single=True),
            series_title=       self.get_element(anime_element, 'series_title',        get_data=True, get_single=True),
            series_type=        self.get_element(anime_element, 'series_type',         get_data=True, get_single=True),
            series_episodes=    self.get_element(anime_element, 'series_episodes',     get_data=True, get_single=True),
            my_id=              self.get_element(anime_element, 'my_id',               get_data=True, get_single=True),
            my_watched_episodes=self.get_element(anime_element, 'my_watched_episodes', get_data=True, get_single=True),
            my_start_date=      self.get_element(anime_element, 'my_start_date',       get_data=True, get_single=True),
            my_finish_date=     self.get_element(anime_element, 'my_finish_date',      get_data=True, get_single=True),
            my_rated=           self.get_element(anime_element, 'my_rated',            get_data=True, get_single=True),
            my_score=           self.get_element(anime_element, 'my_score',            get_data=True, get_single=True),
            my_dvd=             self.get_element(anime_element, 'my_dvd',              get_data=True, get_single=True),
            my_storage=         self.get_element(anime_element, 'my_storage',          get_data=True, get_single=True),
            my_status=          self.get_element(anime_element, 'my_status',           get_data=True, get_single=True),
            my_comments=        self.get_element(anime_element, 'my_comments',         get_data=True, get_single=True),
            my_times_watched=   self.get_element(anime_element, 'my_times_watched',    get_data=True, get_single=True),
            my_rewatch_value=   self.get_element(anime_element, 'my_rewatch_value',    get_data=True, get_single=True),
            my_tags=            self.get_element(anime_element, 'my_tags',             get_data=True, get_single=True),
            my_rewatching=      self.get_element(anime_element, 'my_rewatching',       get_data=True, get_single=True),
            my_rewatching_ep=   self.get_element(anime_element, 'my_rewatching_ep',    get_data=True, get_single=True),
            update_on_import=   self.get_element(anime_element, 'update_on_import',    get_data=True, get_single=True)
        )

    def get_manga_list_object(self, include_current: bool=False, include_onhold: bool=False, include_dropped: bool=False, include_planned: bool=False):
        """ Retrieve user manga list object """
        return List(
            data=[self.get_manga_object(i) for i in self.get_element(self.manga_document, 'manga')],
            include_current=include_current,
            include_onhold=include_onhold,
            include_dropped=include_dropped,
            include_planned=include_planned
        )

    def get_manga_object(self, manga_element: Document):
        """ Retrieve manga object """
        return Manga(
            manga_mangadb_id=    self.get_element(manga_element, 'manga_mangadb_id',     get_data=True, get_single=True),
            manga_title=         self.get_element(manga_element, 'manga_title',          get_data=True, get_single=True),
            manga_volumes=       self.get_element(manga_element, 'manga_volumes',        get_data=True, get_single=True),
            manga_chapters=      self.get_element(manga_element, 'manga_chapters',       get_data=True, get_single=True),
            my_id=               self.get_element(manga_element, 'my_id',                get_data=True, get_single=True),
            my_read_volumes=     self.get_element(manga_element, 'my_read_volumes',      get_data=True, get_single=True),
            my_read_chapters=    self.get_element(manga_element, 'my_read_chapters',     get_data=True, get_single=True),
            my_start_date=       self.get_element(manga_element, 'my_start_date',        get_data=True, get_single=True),
            my_finish_date=      self.get_element(manga_element, 'my_finish_date',       get_data=True, get_single=True),
            my_scanalation_group=self.get_element(manga_element, 'my_scanalation_group', get_data=True, get_single=True),
            my_score=            self.get_element(manga_element, 'my_score',             get_data=True, get_single=True),
            my_storage=          self.get_element(manga_element, 'my_storage',           get_data=True, get_single=True),
            my_status=           self.get_element(manga_element, 'my_status',            get_data=True, get_single=True),
            my_comments=         self.get_element(manga_element, 'my_comments',          get_data=True, get_single=True),
            my_times_read=       self.get_element(manga_element, 'my_times_read',        get_data=True, get_single=True),
            my_tags=             self.get_element(manga_element, 'my_tags',              get_data=True, get_single=True),
            my_reread_value=     self.get_element(manga_element, 'my_reread_value',      get_data=True, get_single=True),
            update_on_import=    self.get_element(manga_element, 'update_on_import',     get_data=True, get_single=True)
        )


class APILoader(Loader):
    """ API Loader class """
    def __init__(self, username: str):
        """ Constructor """
        super().__init__()
        self.username = username

    def create_document(self):
        """ Create document """
        # Documents Initiation
        self.anime_document = list()
        self.manga_document = list()

        # Lambda function
        api_url = lambda list_type, username, offset: API_URL.format(list_type, username, offset)

        # Anime Document
        offset = 0
        response = json.loads(requests.get(api_url(ANIMELIST, self.username, offset)).text)

        while len(response) > 0:
            self.anime_document += response
            offset += len(response)
            response = json.loads(requests.get(api_url(ANIMELIST, self.username, offset)).text)

        # Manga Document
        offset = 0
        response = json.loads(requests.get(api_url(MANGALIST, self.username, offset)).text)

        while len(response) > 0:
            self.manga_document += response
            offset += len(response)
            response = json.loads(requests.get(api_url(MANGALIST, self.username, offset)).text)

    def get_user_object(self, include_current: bool=False, include_onhold: bool=False, include_dropped: bool=False, include_planned: bool=False):
        """ Retrieve user object """
        return User(
            info=self.get_info_object(),
            anime_list=self.get_anime_list_object(
                include_current=include_current,
                include_onhold=include_onhold,
                include_dropped=include_dropped,
                include_planned=include_planned
            ),
            manga_list=self.get_manga_list_object(
                include_current=include_current,
                include_onhold=include_onhold,
                include_dropped=include_dropped,
                include_planned=include_planned
            )
        )

    def get_info_object(self):
        """ Retrieve user information object """
        return Info(
            user_id=None,
            user_name=self.username,
            user_export_type=None
        )

    def get_anime_list_object(self, include_current: bool=False, include_onhold: bool=False, include_dropped: bool=False, include_planned: bool=False):
        """ Retrieve user anime list object """
        return List(
            data=[self.get_anime_object(i) for i in self.anime_document],
            include_current=include_current,
            include_onhold=include_onhold,
            include_dropped=include_dropped,
            include_planned=include_planned
        )

    def get_anime_object(self, anime_data: dict):
        """ Retrieve anime object """
        return Anime(
            series_animedb_id=  anime_data['anime_id'],
            series_title=       anime_data['anime_title'],
            series_type=        anime_data['anime_media_type_string'],
            series_episodes=    anime_data['anime_num_episodes'],
            my_id=              None,
            my_watched_episodes=anime_data['num_watched_episodes'],
            my_start_date=      anime_data['start_date_string'],
            my_finish_date=     anime_data['finish_date_string'],
            my_rated=           None,
            my_score=           anime_data['score'],
            my_dvd=             None,
            my_storage=         anime_data['storage_string'],
            my_status=          ANIME_STATUS_LIST[anime_data['status']],
            my_comments=        None,
            my_times_watched=   None,
            my_rewatch_value=   None,
            my_tags=            anime_data['tags'],
            my_rewatching=      anime_data['is_rewatching'],
            my_rewatching_ep=   None,
            update_on_import=   None
        )

    def get_manga_list_object(self, include_current: bool=False, include_onhold: bool=False, include_dropped: bool=False, include_planned: bool=False):
        """ Retrieve user manga list object """
        return List(
            data=[self.get_manga_object(i) for i in self.manga_document],
            include_current=include_current,
            include_onhold=include_onhold,
            include_dropped=include_dropped,
            include_planned=include_planned
        )

    def get_manga_object(self, manga_data: dict):
        """ Retrieve manga object """
        return Manga(
            manga_mangadb_id=    manga_data['manga_id'],
            manga_title=         manga_data['manga_title'],
            manga_volumes=       manga_data['manga_num_volumes'],
            manga_chapters=      manga_data['manga_num_chapters'],
            my_id=               manga_data['id'],
            my_read_volumes=     manga_data['num_read_volumes'],
            my_read_chapters=    manga_data['num_read_chapters'],
            my_start_date=       manga_data['start_date_string'],
            my_finish_date=      manga_data['finish_date_string'],
            my_scanalation_group=None,
            my_score=            manga_data['score'],
            my_storage=          None,
            my_status=           MANGA_STATUS_LIST[manga_data['status']],
            my_comments=         None,
            my_times_read=       None,
            my_tags=             manga_data['tags'],
            my_reread_value=     None,
            update_on_import=    None
        )
