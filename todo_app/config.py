import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application.")

        self.LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED') == 'True'


        default_log_level = 'INFO' if os.environ.get('FLASK_ENV') == 'development' else 'ERROR'
        self.LOG_LEVEL = os.environ.get('LOG_LEVEL') or default_log_level
