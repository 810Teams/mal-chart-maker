"""
    `data.py`
"""

from src.utils import error
from src.classes.entry import Entry, Anime, Manga

from math import ceil, floor, sqrt


class List:
    """ User anime/manga list class """
    def __init__(
        self,
        data: list=list(),
        include_current: bool=False,
        include_onhold: bool=False,
        include_dropped: bool=False,
        include_planned: bool=False,
        tag_rules: list=None
    ):
        """ Constructor """
        self.data = data
        self.include_current = include_current
        self.include_onhold = include_onhold
        self.include_dropped = include_dropped
        self.include_planned = include_planned
        self.tag_rules = tag_rules

    def add_entry(self, entry: Entry) -> None:
        """ Add anime/manga object to the anime/manga list by object """
        self.data.append(entry)

    def get_entry(self, entry_id: str) -> Entry:
        """ Get anime/manga object from the anime/manga list by anime/manga ID """
        for i in range(len(self.data)):
            if isinstance(self.data[i], Anime) and self.data[i].series_animedb_id == entry_id:
                return self.data[i]
            elif isinstance(self.data[i], Manga) and self.data[i].manga_mangadb_id == entry_id:
                return self.data[i]

        return None

    def delete_entry(self, entry_id: str) -> Entry:
        """ Delete anime/manga object from the anime/manga list by anime/manga ID """
        for i in range(len(self.data)):
            if isinstance(self.data[i], Anime) and self.data[i].series_animedb_id == entry_id:
                return self.data.pop(i)
            elif isinstance(self.data[i], Manga) and self.data[i].manga_mangadb_id == entry_id:
                return self.data.pop(i)

        return None

    def count(self, key: str) -> int:
        """ Count anime/manga with a specific status """
        if key == 'all':
            return len(self.data)
        elif key.title().replace('To', 'to') in ('Watching', 'Reading', 'Completed', 'On-Hold', 'Dropped', 'Plan to Watch', 'Plan to Read'):
            return len([i for i in self.data if i.my_status == key.title().replace('To', 'to')])
        return 0

    def get_list(self, include_unscored: bool=False) -> list:
        """ Get anime/manga list """
        return [
            i for i in self.data
            if (i.my_status != 'Watching' or self.include_current)
            and (i.my_status != 'On-Hold' or self.include_onhold)
            and (i.my_status != 'Dropped' or self.include_dropped)
            and (i.my_status != 'Plan to Watch' or self.include_planned)
            and (i.my_score != 0 or include_unscored)
        ]

    def get_full_list(self, include_unscored: bool=False) -> list:
        """ Get full anime/manga list """
        return [i for i in self.data if i.my_score != 0 or include_unscored]

    def get_grouped_list(
        self,
        include_unscored: bool=False,
        group_by: str='series_type',
        sort_method: str='most_common',
        sort_order: str='descending',
        manual_sort: list=None,
        disassemble_key: str=None
    ) -> dict:
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

    def get_scores(self, include_unscored: bool=False) -> list:
        """ Get anime/manga scores """
        return [i.my_score for i in self.get_list(include_unscored=include_unscored)]

    def get_summed_scores(self, include_unscored: bool=False) -> list:
        """ Get summed anime/manga scores """
        return [
            self.get_scores(include_unscored=include_unscored).count(i)
            for i in range(1 - include_unscored, 11)
        ]

    def get_grouped_scores(
        self,
        include_unscored: bool=False,
        group_by: str='series_type',
        sort_method: str='most_common',
        sort_order: str='descending',
        manual_sort: bool=None
    ) -> dict:
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
        include_unscored: bool=False,
        group_by: str='series_type',
        sort_method: str='most_common',
        sort_order: str='descending',
        manual_sort: bool=None
    ) -> dict:
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

    def get_min(self) -> int:
        """ Get a minimum of the anime/manga list scores """
        return min(self.get_scores())

    def get_max(self) -> int:
        """ Get a maximum of the anime/manga list scores """
        return max(self.get_scores())

    def get_average(self) -> float:
        """ Get an average of the anime/manga list scores """
        scores = self.get_scores()
        return sum(scores) / len(scores)

    def get_median(self) -> int:
        """ Get a median of the anime/manga list scores """
        scores = sorted(self.get_scores())

        if len(scores) % 2 == 0:
            return (scores[len(scores) // 2 - 1] + scores[len(scores) // 2]) / 2
        return scores[len(scores) // 2]

    def get_mode(self) -> int:
        """ Get a mode of the anime/manga list scores """
        return max(self.get_summed_scores())

    def get_sd(self) -> float:
        """ Get a standard deviation of the anime/manga list scores """
        scores = self.get_scores()

        return sqrt(sum([(i - self.get_average()) ** 2 for i in scores]) / len(scores))

    def get_partial(self, percentage: float, part: str='top', rounding_method: str='roundx', include_unscored: bool=False) -> list:
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

    def get_partial_average(self, percentage: float, part: str='top', rounding_method: str='roundx', include_unscored:bool=False) -> float:
        """ Get partial anime/manga list average """
        entry_list = self.get_partial(
            percentage=percentage,
            part=part,
            rounding_method=rounding_method,
            include_unscored=include_unscored
        )
        scores = [i.my_score for i in entry_list]

        return sum(scores)/len(scores)
