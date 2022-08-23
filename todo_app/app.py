from flask import Flask, render_template, request, redirect

from todo_app.data.mongo_items import MongoItems
from todo_app.data.mongo_config import MongoConfig

from todo_app.view_model import ViewModel

def create_app():
    app = Flask(__name__)
    mongo_items = MongoItems(MongoConfig())

    @app.route('/')
    def index():
        items = sorted(mongo_items.get_items(), key=lambda item: item.status == 'Done')
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)


    @app.route('/items', methods=['POST'])
    def add_item():
        mongo_items.add_item(request.form.get('new_item'))
        return redirect('/')


    @app.route('/items/<id>/complete', methods=['POST'])
    def complete_item(id):
        mongo_items.update_status(id, 'Done')
        return redirect('/')

    @app.route('/items/<id>/uncomplete', methods=['POST'])
    def uncomplete_item(id):
        mongo_items.update_status(id, 'To Do')
        return redirect('/')

    return app
