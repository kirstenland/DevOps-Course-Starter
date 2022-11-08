import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application.")

        self.LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED') == 'True'
