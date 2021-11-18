from flask import Flask, render_template, request, redirect

import todo_app.data.session_items as session_items
import todo_app.data.trello_items as trello_items
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = sorted(trello_items.get_items(), key=lambda item: item['status'] == 'Done')
    return render_template('index.html', items=items)


@app.route('/items', methods=['POST'])
def add_item():
    trello_items.add_item(request.form.get('new_item'))
    return redirect('/')


@app.route('/items/<id>/toggle', methods=['POST'])
def toggle_item(id):
    item = session_items.get_item(id)
    item['status'] = ('Not Started' if item['status'] == 'Complete' else 'Complete')
    session_items.save_item(item)
    return redirect('/')
