import os


class OAuthConfig:
    def __init__(self):
        """OAuth configuration variables."""
        self.OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID')
        self.OAUTH_CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET')

        writerIds = os.environ.get('WRITER_USER_IDS')
        self.WRITER_USER_IDS = writerIds.split(',') if writerIds else []
