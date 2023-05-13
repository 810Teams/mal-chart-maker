"""
    `classes/entry.py`
"""


class Entry:
    """ Entry class """
    def __init__(
        self,
        my_id=None,
        my_start_date=None,
        my_finish_date=None,
        my_score=None,
        my_storage=None,
        my_status=None,
        my_comments=None,
        my_tags=None,
        update_on_import=None
    ):
        self.my_id = my_id
        self.my_start_date = my_start_date
        self.my_finish_date = my_finish_date
        self.my_score = my_score
        self.my_storage = my_storage
        self.my_status = my_status
        self.my_comments = my_comments
        self.my_tags = my_tags
        self.update_on_import = update_on_import


class Anime(Entry):
    """ Anime class """
    def __init__(
        self,
        series_animedb_id=None,
        series_title=None,
        series_type=None,
        series_episodes=None,
        my_id=None,
        my_watched_episodes=None,
        my_start_date=None,
        my_finish_date=None,
        my_rated=None,
        my_score=None,
        my_dvd=None,
        my_storage=None,
        my_status=None,
        my_comments=None,
        my_times_watched=None,
        my_rewatch_value=None,
        my_tags=None,
        my_rewatching=None,
        my_rewatching_ep=None,
        update_on_import=None
    ):
        """ Constructor """
        super().__init__(
            my_id=my_id,
            my_start_date=my_start_date,
            my_finish_date=my_finish_date,
            my_score=my_score,
            my_storage=my_storage,
            my_status=my_status,
            my_comments=my_comments,
            my_tags=my_tags,
            update_on_import=update_on_import
        )
        self.series_animedb_id = series_animedb_id
        self.series_title = series_title
        self.series_type = series_type
        self.series_episodes = series_episodes
        self.my_watched_episodes = my_watched_episodes
        self.my_rated = my_rated
        self.my_dvd = my_dvd
        self.my_times_watched = my_times_watched
        self.my_rewatch_value = my_rewatch_value
        self.my_rewatching = my_rewatching
        self.my_rewatching_ep = my_rewatching_ep


class Manga(Entry):
    """ Manga class """
    def __init__(
        self,
        manga_mangadb_id=None,
        manga_title=None,
        manga_volumes=None,
        manga_chapters=None,
        my_id=None,
        my_read_volumes=None,
        my_read_chapters=None,
        my_start_date=None,
        my_finish_date=None,
        my_scanalation_group=None,
        my_score=None,
        my_storage=None,
        my_status=None,
        my_comments=None,
        my_times_read=None,
        my_tags=None,
        my_reread_value=None,
        update_on_import=None
    ):
        """ Constructor """
        super().__init__(
            my_id=my_id,
            my_start_date=my_start_date,
            my_finish_date=my_finish_date,
            my_score=my_score,
            my_storage=my_storage,
            my_status=my_status,
            my_comments=my_comments,
            my_tags=my_tags,
            update_on_import=update_on_import
        )
        self.manga_mangadb_id = manga_mangadb_id
        self.manga_title = manga_title
        self.manga_volumes = manga_volumes
        self.manga_chapters = manga_chapters
        self.my_read_volumes = my_read_volumes
        self.my_read_chapters = my_read_chapters
        self.my_scanalation_group = my_scanalation_group
        self.my_times_read = my_times_read
        self.my_reread_value = my_reread_value
