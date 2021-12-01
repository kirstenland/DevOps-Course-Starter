import os

class TrelloConfig:
    def __init__(self):
        """Trello configuration variables."""
        self.TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
        self.TRELLO_API_TOKEN = os.environ.get('TRELLO_API_TOKEN')
        self.TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
