from flask import Flask, render_template, request, redirect

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


@app.route('/items/<id>/complete', methods=['POST'])
def complete_item(id):
    trello_items.update_status(id, 'Done')
    return redirect('/')

@app.route('/items/<id>/uncomplete', methods=['POST'])
def uncomplete_item(id):
    trello_items.update_status(id, 'To Do')
    return redirect('/')
