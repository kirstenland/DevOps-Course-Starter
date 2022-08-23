import os

class MongoConfig:
    def __init__(self):
        """Mongo configuration variables."""
        self.MONGO_CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING')
        self.MONGO_DATABASE_NAME = os.environ.get('MONGO_DATABASE_NAME')
        self.MONGO_COLLECTION_NAME = os.environ.get('MONGO_COLLECTION_NAME')
