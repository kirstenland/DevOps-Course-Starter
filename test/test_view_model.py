import pytest

from todo_app.data.item import Item
from todo_app.view_model import ViewModel

def test_items_are_stored_in_view_model():
    items = [Item(1, 'Test Item', 'Done'), Item(2, 'Another Test Item', 'To Do')]
    view_model = ViewModel(items)
    assert view_model.items == items

