"""
    `data.py`
"""

from src.utils import error

from math import ceil, floor, sqrt


class User:
    """ User class """
    def __init__(self, info, anime_list, manga_list, do_refresh=True):
        """ Constructor """
        self.info = info
        self.anime_list = anime_list
        self.manga_list = manga_list


class Info:
    """ User information class """
    def __init__(
        self,
        user_id,
        user_name,
        user_export_type
    ):
        """ Constructor """
        self.user_id = user_id
        self.user_name = user_name
        self.user_export_type = user_export_type


class List:
    """ User anime/manga list class """
    def __init__(
        self,
        data=list(),
        include_current=False,
        include_onhold=False,
        include_dropped=False,
        include_planned=False,
        tag_rules=None
    ):
        """ Constructor """
        self.data = data
        self.include_current = include_current
        self.include_onhold = include_onhold
        self.include_dropped = include_dropped
        self.include_planned = include_planned
        self.tag_rules = tag_rules

    def add_entry(self, entry):
        """ Add anime/manga object to the anime/manga list by object """
        self.data.append(entry)

    def get_entry(self, entry_id):
        """ Get anime/manga object from the anime/manga list by anime/manga ID """
        for i in range(len(self.data)):
            if isinstance(self.data[i], Anime) and self.data[i].series_animedb_id == entry_id:
                return self.data[i]
            elif isinstance(self.data[i], Manga) and self.data[i].manga_mangadb_id == entry_id:
                return self.data[i]

        return None

    def delete_entry(self, entry_id):
        """ Delete anime/manga object from the anime/manga list by anime/manga ID """
        for i in range(len(self.data)):
            if isinstance(self.data[i], Anime) and self.data[i].series_animedb_id == entry_id:
                return self.data.pop(i)
            elif isinstance(self.data[i], Manga) and self.data[i].manga_mangadb_id == entry_id:
                return self.data.pop(i)

        return None

    def count(self, key):
        """ Count anime/manga with a specific status """
        if key == 'all':
            return len(self.data)
        elif key.title().replace('To', 'to') in ('Watching', 'Reading', 'Completed', 'On-Hold', 'Dropped', 'Plan to Watch', 'Plan to Read'):
            return len([i for i in self.data if i.my_status == key.title().replace('To', 'to')])
        return 0

    def get_list(self, include_unscored=False):
        """ Get anime/manga list """
        return [
            i for i in self.data
            if (i.my_status != 'Watching' or self.include_current)
            and (i.my_status != 'On-Hold' or self.include_onhold)
            and (i.my_status != 'Dropped' or self.include_dropped)
            and (i.my_status != 'Plan to Watch' or self.include_planned)
            and (i.my_score != 0 or include_unscored)
        ]

    def get_full_list(self, include_unscored=False):
        """ Get full anime/manga list """
        return [i for i in self.data if i.my_score != 0 or include_unscored]

    def get_grouped_list(
        self,
        include_unscored=False,
        group_by='series_type',
        sort_method='most_common',
        sort_order='descending',
        manual_sort=None,
        disassemble_key=None
    ):
        """ Get grouped anime/manga list """
        grouped_entry_list = dict()
        categories = list()

        filtered_entry_list = self.get_list(include_unscored=include_unscored)

        # Category Retrieval
        for _ in filtered_entry_list:
            if eval('_.{}'.format(group_by)) not in categories:
                categories.append(eval('_.{}'.format(group_by)))

        # Category Sorting
        if sort_method == 'most_common':
            categories.sort(
                key=lambda i: [eval('j.{}'.format(group_by)) for j in filtered_entry_list].count(i),
                reverse=sort_order != 'ascending'
            )
        elif sort_method == 'alphabetical':
            categories.sort(
                reverse=sort_order != 'ascending'
            )
        else:
            error('Invalid sort_method `{}` of get_grouped_list().'.format(sort_method))
            return None

        # Manual Sort Override
        if manual_sort != None:
            old_categories = [i for i in categories]
            categories = list()

            for i in manual_sort:
                if i in old_categories:
                    categories.append(i)
                    old_categories.remove(i)

            categories += old_categories

        # Packing Categories
        for i in categories:
            grouped_entry_list[i] = [j for j in filtered_entry_list if eval('j.{}'.format(group_by)) == i]

        # Desired Data Retrieval
        if disassemble_key != None:
            for i in grouped_entry_list:
                for j in range(len(grouped_entry_list[i])):
                    temp = ['grouped_entry_list[i][j].{}'.format(k) for k in disassemble_key]
                    for k in range(len(temp)):
                        temp[k] = eval(temp[k])
                    grouped_entry_list[i][j] = temp

        # Return
        return grouped_entry_list

    def get_scores(self, include_unscored=False):
        """ Get anime/manga scores """
        return [i.my_score for i in self.get_list(include_unscored=include_unscored)]

    def get_summed_scores(self, include_unscored=False):
        """ Get summed anime/manga scores """
        return [
            self.get_scores(include_unscored=include_unscored).count(i)
            for i in range(1 - include_unscored, 11)
        ]

    def get_grouped_scores(
        self,
        include_unscored=False,
        group_by='series_type',
        sort_method='most_common',
        sort_order='descending',
        manual_sort=None
    ):
        """ Get grouped anime/manga scores """
        grouped_entry_list = self.get_grouped_list(
            include_unscored=False,
            group_by=group_by,
            sort_method=sort_method,
            sort_order=sort_order,
            manual_sort=manual_sort
        )

        for i in grouped_entry_list:
            for j in range(len(grouped_entry_list[i])):
                grouped_entry_list[i][j] = grouped_entry_list[i][j].my_score

        return grouped_entry_list

    def get_summed_grouped_scores(
        self,
        include_unscored=False,
        group_by='series_type',
        sort_method='most_common',
        sort_order='descending',
        manual_sort=None
    ):
        """ Get summed grouped anime/manga scores """
        scores = self.get_grouped_scores(
            include_unscored=include_unscored,
            group_by=group_by,
            sort_method=sort_method,
            sort_order=sort_order,
            manual_sort=manual_sort
        )

        for i in scores:
            scores[i] = [scores[i].count(j) for j in range(1 - include_unscored, 11)]

        return scores

    def get_min(self):
        """ Get a minimum of the anime/manga list scores """
        return min(self.get_scores())

    def get_max(self):
        """ Get a maximum of the anime/manga list scores """
        return max(self.get_scores())

    def get_average(self):
        """ Get an average of the anime/manga list scores """
        scores = self.get_scores()
        return sum(scores) / len(scores)

    def get_median(self):
        """ Get a median of the anime/manga list scores """
        scores = sorted(self.get_scores())

        if len(scores) % 2 == 0:
            return (scores[len(scores) // 2 - 1] + scores[len(scores) // 2]) / 2
        return scores[len(scores) // 2]

    def get_mode(self):
        """ Get a mode of the anime/manga list scores """
        return max(self.get_summed_scores())

    def get_sd(self):
        """ Get a standard deviation of the anime/manga list scores """
        scores = self.get_scores()

        return sqrt(sum([(i - self.get_average()) ** 2 for i in scores]) / len(scores))

    def get_partial(self, percentage, part='top', rounding_method='roundx', include_unscored=False):
        """ Get partial anime/manga list """
        # Anime/manga List Initiation
        entry_list = self.get_list(include_unscored=include_unscored)
        entry_list.sort(key=lambda i: i.my_score, reverse=True)

        # Anime/manga Count Calculation
        entry_count = percentage / 100 * len(entry_list)

        # Anime/manga Count Rounding Method
        if rounding_method == 'floor':
            entry_count = floor(entry_count)
        elif rounding_method == 'ceil':
            entry_count = ceil(entry_count)
        elif rounding_method == 'round':
            entry_count = round(entry_count)
        elif rounding_method == 'roundx':
            if entry_count % 0.5 == 0:
                entry_count = floor(entry_count)
            else:
                entry_count = round(entry_count)
        else:
            error('Invalid rounding_method `{}` of get_partial().'.format(rounding_method))
            return None

        # Anime/manga List Slicing
        if part == 'top':
            return entry_list[:entry_count]
        elif part == 'bottom':
            entry_list.reverse()
            return entry_list[:entry_count]
        elif part == 'middle':
            middle = len(entry_list)//2
            upper = middle + floor(entry_count/2)
            lower = middle - ceil(entry_count/2)

            return entry_list[lower:upper]
        else:
            error('Invalid part `{}` of get_partial().'.format(part))
            return None

    def get_partial_average(self, percentage, part='top', rounding_method='roundx', include_unscored=False):
        """ Get partial anime/manga list average """
        entry_list = self.get_partial(
            percentage=percentage,
            part=part,
            rounding_method=rounding_method,
            include_unscored=include_unscored
        )
        scores = [i.my_score for i in entry_list]

        return sum(scores)/len(scores)


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
