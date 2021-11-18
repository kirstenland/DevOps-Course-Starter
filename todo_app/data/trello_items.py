import requests

from todo_app.data.trello_config import TrelloConfig

CONFIG = TrelloConfig()
TRELLO_BASE_URL = "https://api.trello.com"

def get_auth_params():
    return {
        "key": CONFIG.TRELLO_API_KEY,
        "token": CONFIG.TRELLO_API_TOKEN
    }

def get_items():
    """
    Fetches all saved items from trello.

    Returns:
        list: The list of saved items.
    """
    get_items_url = TRELLO_BASE_URL + "/1/boards/" + CONFIG.TRELLO_BOARD_ID + "/lists"
    full_params = get_auth_params() | { 'cards': 'open' }
    results = requests.get(get_items_url, params=full_params).json()
    mapped_items = [{ 'id': card['id'], 'title': card['name'], 'status': list['name'] } for list in results for card in list['cards']]
    return mapped_items
