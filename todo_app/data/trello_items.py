import requests
from todo_app.data.Item import Item

from todo_app.data.trello_config import TrelloConfig

CONFIG = TrelloConfig()
TRELLO_BASE_URL = "https://api.trello.com/1"

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
    get_lists_url = TRELLO_BASE_URL + "/boards/" + CONFIG.TRELLO_BOARD_ID + "/lists"
    full_params = get_auth_params() | { 'cards': 'open' }
    results = requests.get(get_lists_url, params=full_params).json()
    mapped_items = [Item.from_trello_card(card, trello_list) for trello_list in results for card in trello_list['cards']]
    return mapped_items

def add_item(title):
    """
    Adds a new item with the specified title to trello.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    list_name = 'To Do'
    trello_list = get_list_by_name(list_name)

    create_card_url = TRELLO_BASE_URL + "/cards"
    request_body = {
        'idList': trello_list['id'],
        'name': title
    }

    new_card = requests.post(
        create_card_url,
        params=get_auth_params(),
        data=request_body
    ).json()

    return Item.from_trello_card(new_card, trello_list)

def update_status(item_id, new_status):
    """
    Updates the status of the specified item

    Args:
        item_id: The id of the item.
        new_status: The desired new status of the item.

    Returns:
        item: The updated item.
    """
    trello_list = get_list_by_name(new_status)

    edit_card_url = TRELLO_BASE_URL + "/cards/" + item_id
    request_body = {
        'idList': trello_list['id'],
    }

    updated_card = requests.put(
        edit_card_url,
        params=get_auth_params(),
        data=request_body
    ).json()

    return Item.from_trello_card(updated_card, trello_list)

def get_list_by_name(name):
    get_lists_url = TRELLO_BASE_URL + "/boards/" + CONFIG.TRELLO_BOARD_ID + "/lists"
    trello_lists = requests.get(get_lists_url, params=get_auth_params()).json()
    trello_list = [trello_list for trello_list in trello_lists if trello_list['name'] == name][0]

    return trello_list
