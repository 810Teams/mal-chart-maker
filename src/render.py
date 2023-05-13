"""
    render.py
"""

from math import ceil, floor
from pygal.style import Style, DefaultStyle
from pygal import Graph

from src.utils import notice

import pygal


class RenderMachine:
    def __init__(
        self,
        chart_dir: str,
        legend_at_bottom: bool=False,
        legend_box_size: int=15,
        max_y_labels: int=15,
        style: Style=DefaultStyle,
        y_labels_preset: tuple=(1, 2, 5),
        y_labels_skip: bool=False
    ):
        self.chart_dir = chart_dir
        self.legend_at_bottom = legend_at_bottom
        self.legend_box_size = legend_box_size
        self.max_y_labels = max_y_labels
        self.style = style
        self.y_labels_preset = y_labels_preset
        self.y_labels_skip = y_labels_skip

    def render_pie_chart(self, data: list, file_name: str='untitled_chart', title: str=str()):
        """ Function: Render pie chart """
        # Chart Initialization
        chart = pygal.Pie()

        # Chart Data
        total = sum([len(data[category]) for category in data])
        for category in data:
            chart.add(str(category), [{
                    'value': len(data[category]),
                    'label': '{}/{} ({:.2f}%)'.format(len(data[category]), total, 100 * len(data[category]) / total)
                }]
            )

        # Finish Chart
        self.finish_chart(chart, file_name=file_name, show_legend=True, title=title)

    def render_bar_chart(self, data, file_name: str='untitled_chart', title: str=str()):
        """ Function: Render bar chart """
        # Chart Initialization
        chart = pygal.HorizontalStackedBar()

        # Chart Data
        if isinstance(data, list):
            total = sum(data)
            chart.add('Scored', [
                {'value': i, 'label': '{}/{} ({:.2f}%)'.format(i, total, 100 * i / total)}
                for i in data
            ])
        elif isinstance(data, dict):
            total = sum([sum(data[category]) for category in data])
            for category in data:
                chart.add(category, [
                    {'value': i, 'label': '{}/{} ({:.2f}%)'.format(i, total, 100 * i / total)}
                    for i in data[category]
                ])

        # Chart Labels
        if isinstance(data, list):
            chart.x_labels = [i for i in range(1 - (len(data) == 11), 11, 1)]
            chart.y_labels = self.get_y_labels(0, max(data))
        elif isinstance(data, dict):
            chart.x_labels = [i for i in range(1 - (len(data[[j for j in data][0]]) == 11), 11, 1)]
            data_r = [data[i] for i in data]
            data_r = [[data_r[j][i] for j in range(len(data_r))] for i in range(len(data_r[0]))]
            data_r = [sum(i) for i in data_r]
            chart.y_labels = self.get_y_labels(0, max(data_r))

        # Finish Chart
        self.finish_chart(chart, file_name=file_name, show_legend=isinstance(data, dict), title=title)

    def render_treemap(self, data, value: int=0, label: int=1, ignore_value: bool=False, file_name: str='untitled_chart', title: str=str()):
        """ Function: renders Treemap chart """
        # Chart Initialization
        chart = pygal.Treemap()

        # Chart Data
        if isinstance(data, list):
            chart.add('Anime', [{'value': i[value] * (not ignore_value) + ignore_value, 'label': str(i[label])} for i in data])
        elif isinstance(data, dict):
            for category in data:
                chart.add(str(category), [{'value': i[value] * (not ignore_value) + ignore_value, 'label': str(i[label])} for i in data[category]])

        # Finish Chart
        self.finish_chart(chart, file_name=file_name, show_legend=isinstance(data, dict), title=title)

    def finish_chart(self, chart: Graph, file_name: str='untitled_chart', show_legend: bool=True, title: str=str()):
        """ Function: Common chart setup and rendering steps """
        # Chart Titles
        chart.title = title

        # Chart Legends
        chart.show_legend = show_legend
        chart.legend_at_bottom = self.legend_at_bottom
        chart.legend_box_size = self.legend_box_size

        # Chart Render
        chart.style = self.style
        chart.render_to_file(
            '{}{}{}.svg'.format(
                self.chart_dir,
                '/' * (self.chart_dir[-1] != '/'),
                file_name.replace('.svg', '')
            )
        )

        # Notice
        notice('Chart \'{}\' successfully exported.'.format(file_name))

    def get_y_labels(self, data_min: float, data_max: float):
        """ Function: Calculates y-labels of the chart """
        data_min = floor(data_min)
        data_max = ceil(data_max)

        preset = self.y_labels_preset
        i = 0

        if not self.y_labels_skip:
            data_range = list(range(0, data_min - 1, -1)) + list(range(0, data_max + 1, 1))

            while len(data_range) > self.max_y_labels:
                data_range = list(range(0, data_min - preset[i % 3] * 10 ** (i // 3), -1 * preset[i % 3] * 10 ** (i // 3)))
                data_range += list(range(0, data_max + preset[i % 3] * 10 ** (i // 3), preset[i % 3] * 10 ** (i // 3)))
                i += 1
        else:
            data_min = int(data_min/10) * 10
            data_range = list(range(data_min, data_max + 1, 1))

            while len(data_range) > self.max_y_labels:
                data_range = list(range(data_min, data_max + preset[i % 3] * 10 ** (i // 3), preset[i % 3] * 10 ** (i // 3)))
                i += 1

        data_range.sort()

        return data_range
