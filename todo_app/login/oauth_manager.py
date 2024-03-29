import urllib
import requests
from todo_app.login.error import GithubRequestFailedException, handle_github_request_errors

from todo_app.login.user import User
from todo_app.login.authorization import WRITER, READER


class OAuthManager():
    def __init__(self, config):
        self._config = config

    def get_authorize_url(self):
        url = 'https://github.com/login/oauth/authorize/'
        params = {
            'client_id': self._config.OAUTH_CLIENT_ID
        }

        return '{}?{}'.format(url, urllib.parse.urlencode(params))

    def get_token(self, code):
        url = 'https://github.com/login/oauth/access_token'
        params = {
            'client_id': self._config.OAUTH_CLIENT_ID,
            'client_secret': self._config.OAUTH_CLIENT_SECRET,
            'code': code
        }
        headers = {'Accept': 'application/json'}
        response = requests.post(url, params=params, headers=headers).json()

        handle_github_request_errors(response, 'get token from code')

        return response['access_token']

    def get_user(self, token):
        response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': 'Bearer ' + token}
        ).json()

        handle_github_request_errors(response, 'get user from token')

        id = response['id']
        return User(id, self.get_role(id))

    def get_role(self, user_id):
        if user_id in self._config.WRITER_USER_IDS:
            return WRITER
        return READER
