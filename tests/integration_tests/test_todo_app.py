from datetime import datetime
import pytest
import mongomock
import pymongo
from dotenv import load_dotenv, find_dotenv

from todo_app import app
from todo_app.data.mongo_config import MongoConfig

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def get_db():
    mongo_config = MongoConfig()
    return pymongo.MongoClient(mongo_config.MONGO_CONNECTION_STRING)[mongo_config.MONGO_DATABASE_NAME]

def when_db_contains_test_card():
    get_db().todos.insert_one({
        'title': 'Test card',
        'last_modified': datetime.utcnow(),
        'status': 'To Do'
    })

def test_index_page(client):
    when_db_contains_test_card()
    response = client.get('/')
    assert response.status_code == 200
    assert 'Test card' in response.data.decode() 
