import pytest

from todo_app.data.item import Item
from todo_app.view_model import ViewModel

def test_items_are_stored_in_view_model():
    items = [Item(1, 'Test Item', 'Done'), Item(2, 'Another Test Item', 'To Do')]
    view_model = ViewModel(items)
    assert view_model.items == items


def test_to_do_items_returns_only_items_with_status_to_do_in_order():
    items = [Item(1, 'Test Item', 'To Do'), Item(2, 'Another Test Item', 'Done'), Item(3, 'A third Test Item', 'To Do')]
    view_model = ViewModel(items)
    assert view_model.to_do_items == [items[0], items[2]]


def test_to_do_items_returns_empty_list_if_all_items_are_done():
    items = [Item(1, 'Test Item', 'Done'), Item(2, 'Another Test Item', 'Done')]
    view_model = ViewModel(items)
    assert view_model.to_do_items == []


def test_doing_items_returns_only_items_with_status_doing_in_order():
    items = [
        Item(1, 'Test Item', 'To Do'),
        Item(2, 'Another Test Item', 'Done'),
        Item(3, 'A third Test Item', 'Doing'),
        Item(3, 'A final Test Item', 'Doing'),
    ]
    view_model = ViewModel(items)
    assert view_model.doing_items == [items[2], items[3]]


def test_doing_items_returns_empty_list_if_all_items_are_done_or_to_do():
    items = [Item(1, 'Test Item', 'To Do'), Item(2, 'Another Test Item', 'Done')]
    view_model = ViewModel(items)
    assert view_model.doing_items == []


def test_done_items_returns_only_items_with_status_done_in_order():
    items = [
        Item(1, 'Test Item', 'To Do'),
        Item(2, 'Another Test Item', 'Done'),
        Item(3, 'A third Test Item', 'Doing'),
        Item(3, 'A final Test Item', 'Done'),
    ]
    view_model = ViewModel(items)
    assert view_model.done_items == [items[1], items[3]]


def test_doing_items_returns_empty_list_if_all_items_are_to_do_or_doing():
    items = [Item(1, 'Test Item', 'To Do'), Item(2, 'Another Test Item', 'Doing')]
    view_model = ViewModel(items)
    assert view_model.done_items == []

