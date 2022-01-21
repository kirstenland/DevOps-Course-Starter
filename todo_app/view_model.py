from datetime import datetime, date


class ViewModel:
    def __init__(self, items):
        self._items = items
    
    @property
    def items(self):
        return self._items
    
    @property
    def to_do_items(self):
        return [item for item in self._items if item.status == 'To Do']

    @property
    def done_items(self):
        return [item for item in self._items if item.status == 'Done']
    
    @property
    def should_show_all_done_items(self):
        return len(self.done_items) < 5

    @property
    def recent_done_items(self):
        return [item for item in self.done_items if item.last_modified.date() == date.today()]

    @property
    def older_done_items(self):
        return [item for item in self.done_items if item.last_modified.date() != date.today()]
    
    @property
    def done_items_always_shown(self):
        return self.done_items if self.should_show_all_done_items else self.recent_done_items
