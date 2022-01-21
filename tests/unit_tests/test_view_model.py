from datetime import datetime, timedelta
import pytest

from todo_app.data.item import Item
from todo_app.view_model import ViewModel

def test_items_are_stored_in_view_model():
    items = [done_item(1), to_do_item(2)]
    view_model = ViewModel(items)
    assert view_model.items == items


def test_to_do_items_returns_only_items_with_status_to_do_in_order():
    items = [to_do_item(1), done_item(2), to_do_item(3)]
    view_model = ViewModel(items)
    assert view_model.to_do_items == [items[0], items[2]]


def test_to_do_items_returns_empty_list_if_all_items_are_done():
    items = [done_item(1), done_item(2)]
    view_model = ViewModel(items)
    assert view_model.to_do_items == []


def test_doing_items_returns_only_items_with_status_doing_in_order():
    items = [
        Item(1, 'Test Item', 'To Do', datetime.now()),
        Item(2, 'Another Test Item', 'Done', datetime.now()),
        Item(3, 'A third Test Item', 'Doing', datetime.now()),
        Item(3, 'A final Test Item', 'Doing', datetime.now()),
    ]
    view_model = ViewModel(items)
    assert view_model.doing_items == [items[2], items[3]]


def test_doing_items_returns_empty_list_if_all_items_are_done_or_to_do():
    items = [to_do_item(1), done_item(2)]
    view_model = ViewModel(items)
    assert view_model.doing_items == []


def test_done_items_returns_only_items_with_status_done_in_order():
    items = [
        to_do_item(1),
        done_item(2),
        to_do_item(3),
        done_item(4),
    ]
    view_model = ViewModel(items)
    assert view_model.done_items == [items[1], items[3]]


def test_doing_items_returns_empty_list_if_all_items_are_to_do_or_doing():
    items = [to_do_item(1), to_do_item(2)]
    view_model = ViewModel(items)
    assert view_model.done_items == []


def test_should_show_all_done_items_if_there_are_less_than_five_done_items():
    items = [done_item(i) for i in range(3)]
    view_model = ViewModel(items)
    assert view_model.should_show_all_done_items


def test_should_not_show_all_done_items_if_there_are_five_done_items():
    items = [done_item(i) for i in range(5)]
    view_model = ViewModel(items)
    assert not view_model.should_show_all_done_items


def test_should_not_show_all_done_items_if_there_are_more_than_five_done_items():
    items = [done_item(i) for i in range(10)]
    view_model = ViewModel(items)
    assert not view_model.should_show_all_done_items

def test_does_not_count_todo_items_towards_the_five_done_items_limit():
    items = [done_item(i) for i in range(4)] + [to_do_item(i + 4) for i in range(10)]
    view_model = ViewModel(items)
    assert view_model.should_show_all_done_items

def test_recent_done_items_includes_items_last_modified_today():
    recent_item = done_item(1, datetime.now())
    items = [recent_item]
    view_model = ViewModel(items)
    assert recent_item in view_model.recent_done_items


def test_recent_done_items_excludes_items_last_modified_yesterday():
    yesterday_item = done_item(1, datetime.now() - timedelta(days=1))
    items = [yesterday_item]
    view_model = ViewModel(items)
    assert not yesterday_item in view_model.recent_done_items


def test_recent_done_items_excludes_items_last_modified_late_yesterday():
    now = datetime.now()
    hours_since_10_pm_yesterday = 2 + now.hour
    late_yesterday = now - timedelta(days=1, hours=hours_since_10_pm_yesterday)
    late_yesterday_item = done_item(1, late_yesterday)
    items = [late_yesterday_item]
    view_model = ViewModel(items)
    assert not late_yesterday_item in view_model.recent_done_items


def test_older_done_items_excludes_items_last_modified_today():
    recent_item = done_item(1, datetime.now())
    items = [recent_item]
    view_model = ViewModel(items)
    assert not recent_item in view_model.older_done_items


def test_recent_done_items_excludes_items_last_modified_yesterday():
    yesterday_item = done_item(1, datetime.now() - timedelta(days=1))
    items = [yesterday_item]
    view_model = ViewModel(items)
    assert yesterday_item in view_model.older_done_items


def test_recent_done_items_excludes_items_last_modified_late_yesterday():
    now = datetime.now()
    hours_since_10_pm_yesterday = 2 + now.hour
    late_yesterday = now - timedelta(days=1, hours=hours_since_10_pm_yesterday)
    late_yesterday_item = done_item(1, late_yesterday)
    items = [late_yesterday_item]
    view_model = ViewModel(items)
    assert late_yesterday_item in view_model.older_done_items


def done_item(index, last_modified = None):
    last_modified = last_modified or datetime.now()
    return Item(index, 'Test Item', 'Done', last_modified)


def to_do_item(index, last_modified = None):
    last_modified = last_modified or datetime.now()
    return Item(index, 'Test Item', 'To Do', last_modified)
