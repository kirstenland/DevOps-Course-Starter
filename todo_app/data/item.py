from datetime import datetime

class Item:
    def __init__(self, id, title, status, last_modified):
        self.id = id
        self.title = title
        self.status = status
        self.last_modified = last_modified

    @classmethod
    def from_trello_card(cls, card, trello_list):
        return cls(card['id'], card['name'], trello_list['name'], datetime.strptime(card['dateLastActivity'], "%Y-%m-%dT%H:%M:%S.%fZ"))

