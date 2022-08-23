from os import stat
from pydoc import cli
import pymongo
from bson.objectid import ObjectId
import datetime

from todo_app.data.item import Item

class MongoItems():
    def __init__(self, config):
        self._config = config

    def with_auth_params(self, params):
        return { **self.get_auth_params(), **params }

    def get_items(self):
        """
        Fetches all saved items from the mongo collection.

        Returns:
            list: The list of saved items.
        """
        results = self.get_db().todos.find()
        mapped_items = [Item.from_mongo_item(item) for item in results]
        return mapped_items

    def add_item(self, title):
        """
        Adds a new item with the specified title and status 'To Do' to the collections.

        Args:
            title: The title of the item.
        """
        status = 'To Do'
        item = {
            'title': title,
            'status': status,
            'last_modified': datetime.datetime.utcnow(),
        }

        self.get_db().todos.insert_one(item)

    def update_status(self, item_id, new_status):
        """
        Updates the status of the specified item

        Args:
            item_id: The id of the item.
            new_status: The desired new status of the item.
        """
        self.get_db().todos.find_one_and_update(
            { '_id': ObjectId(item_id) },
            {
                '$set': {
                    'status': new_status,
                    'last_modified': datetime.datetime.utcnow(),
                },
            },
        )

    def get_db(self):
        client = pymongo.MongoClient(self._config.MONGO_CONNECTION_STRING)
        database = client[self._config.MONGO_DATABASE_NAME]
        return database
