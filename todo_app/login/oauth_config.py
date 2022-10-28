import os


class OAuthConfig:
    def __init__(self):
        """OAuth configuration variables."""
        self.OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID')
        self.OAUTH_CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET')
