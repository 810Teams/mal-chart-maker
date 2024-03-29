"""
    `utils.py`
"""


def error(message: str, show: bool=True, end: str='\n'):
    """ Display error message """
    if show:
        print('[ERROR]', message, end=end)


def log(message: str, show: bool=True, end: str='\n'):
    """ Display log message """
    if show:
        print('[LOG]', message, end=end)


def notice(message: str, show: bool=True, end: str='\n'):
    """ Display notice message """
    if show:
        print('[NOTICE]', message, end=end)
