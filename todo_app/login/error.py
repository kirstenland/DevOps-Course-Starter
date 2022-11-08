class GithubRequestFailedException(Exception):
    def __init__(self, attempted_action, error, error_description, error_uri):
        self.message = 'Failed to {attempted_action}'.format(
            attempted_action=attempted_action
        )
        self.attempted_action = attempted_action
        self.github_error = error
        self.github_error_description = error_description
        self.github_error_uri = error_uri


def handle_github_request_errors(response_body, attempted_action):
    if 'error' in response_body:
        raise GithubRequestFailedException(
            attempted_action,
            response_body.get('error'),
            response_body.get('error_description'),
            response_body.get('error_uri'))
