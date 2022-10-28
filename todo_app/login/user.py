from tkinter import WRITABLE
from flask_login import UserMixin

from todo_app.login.authorization import WRITER


class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

    @property
    def can_write(self):
        return self.role == WRITER
