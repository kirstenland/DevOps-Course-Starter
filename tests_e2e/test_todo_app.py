import os
from turtle import done
from dotenv import load_dotenv, find_dotenv
from threading import Thread
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from tests_e2e.trello_board_helpers import create_trello_board, delete_trello_board
from todo_app import app

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        # Wait up to 2 seconds when looking for an element
        driver.implicitly_wait(2)

        yield driver


@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    # Create the new board & update the board id environment variable
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)

def test_task_journey(driver, app_with_temp_board):
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
