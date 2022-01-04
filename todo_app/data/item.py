class Item:
    def __init__(self, id, title, status = 'To Do'):
        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def from_trello_card(cls, card, trello_list):
        return cls(card['id'], card['name'], trello_list['name'])