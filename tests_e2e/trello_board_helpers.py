import requests
import os

TRELLO_BASE_URL = "https://api.trello.com/1"

def get_auth_params():
    return {
        "key": os.environ.get('TRELLO_API_KEY'),
        "token": os.environ.get('TRELLO_API_TOKEN')
    }


def create_trello_board():
    create_board_url = TRELLO_BASE_URL + "/boards/"
    board_info = {
        'name': 'Test Board',
        'idOrganization': os.environ.get('TRELLO_ORGANIZATION_ID'),
    }
    board = requests.post(create_board_url, params=get_auth_params(), data=board_info).json()

    return board['id']

def delete_trello_board(id):
    delete_board_url = TRELLO_BASE_URL + "/boards/" + str(id)
    requests.delete(delete_board_url, params=get_auth_params())
