class Item:
    def __init__(self, id, title, status, last_modified):
        self.id = id
        self.title = title
        self.status = status
        self.last_modified = last_modified

    @classmethod
    def from_mongo_item(cls, item):
        return cls(str(item['_id']), item['title'], item['status'], item['last_modified'])
