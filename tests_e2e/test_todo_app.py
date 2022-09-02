import os
from time import sleep
import uuid
from dotenv import load_dotenv, find_dotenv
from threading import Thread
import pymongo
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from todo_app import app

@pytest.fixture(scope='module')
def driver():
    opts = Options()
    opts.headless = True
    with webdriver.Firefox(options=opts) as driver:
         # Wait up to 10 seconds when looking for an element
        driver.implicitly_wait(10)

        yield driver

@pytest.fixture(scope='module')
def app_with_temp_db():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    # Update the database name to use a random test database so concurrent tests do not interfere
    database_name = 'test_database_'+str(uuid.uuid1())[:5]
    os.environ['MONGO_DATABASE_NAME'] = database_name
    os.environ['LOGIN_DISABLED'] = 'True'
    client = pymongo.MongoClient(os.environ['MONGO_CONNECTION_STRING'])

    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()

    # Wait for application to load
    sleep(1)

    yield application

    # Tear Down
    thread.join(1)
    client.drop_database(os.environ['MONGO_DATABASE_NAME'])

def test_task_journey(driver, app_with_temp_db):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    new_item_input = driver.find_element(By.NAME, 'new_item')
    new_item_input.clear()
    new_item_input.send_keys('Test my application')
    new_item_input.send_keys(Keys.RETURN)

    list_item = driver.find_element(By.CLASS_NAME, 'to-do-item')
    assert list_item.text == 'Test my application'

    checkbox = driver.find_element(By.CLASS_NAME, 'form-check-input')
    checkbox.click()

    done_items = driver.find_elements(By.CLASS_NAME, 'done-item')
    assert 'Test my application' in [item.text for item in done_items]
