'''
    `utils.py`
'''


def error(message, show=True, end='\n'):
    ''' Display error message '''
    if show:
        print('[ERROR]', message, end=end)


def log(message, show=True, end='\n'):
    ''' Display log message '''
    if show:
        print('[LOG]', message, end=end)


def notice(message, show=True, end='\n'):
    ''' Display notice message '''
    if show:
        print('[NOTICE]', message, end=end)
        