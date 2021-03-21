# Settings

from pygal.style import *


# Overall
# - API Usage
USE_API = True
MAL_USERNAME = '810Teams'


# Main Script
# - Status Displaying
DISPLAY_ANIME_STATS = True
DISPLAY_MANGA_STATS = True

# - Tags
ENABLE_TAG_VALIDATIONS = False
MUST_BE_TAGGED = ('Watching', 'Completed', 'On-Hold')
MUST_BE_UNTAGGED = ('Dropped', 'Planned')
APPLY_TAG_RULES = ('Watching', 'Completed', 'On-Hold')

# - Chart
CHART_STYLE = DarkStyle
MANUAL_SORT_ANIME = ['TV', 'Movie', 'Special', 'OVA', 'ONA', 'Music']
ENABLE_AUTO_CHART_OPEN = False


# CSS Minification
CSS_NAME = 'brink-1.4.3'
CSS_PATH = 'css/{}.css'.format(CSS_NAME)
MIN_CSS_PATH = 'css/{}.min.css'.format(CSS_NAME)
