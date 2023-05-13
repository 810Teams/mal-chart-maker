"""
    `classes/info.py`
"""


class Info:
    """ User information class """
    def __init__(
        self,
        user_id: str,
        user_name: str,
        user_export_type: str
    ):
        """ Constructor """
        self.user_id = user_id
        self.user_name = user_name
        self.user_export_type = user_export_type
