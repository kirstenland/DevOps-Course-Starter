from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user
import requests
from todo_app.login.authorization import current_user_can_write, writer_required

from todo_app.login.user import User

from todo_app.data.mongo_items import MongoItems
from todo_app.data.mongo_config import MongoConfig

from todo_app.login.oauth_config import OAuthConfig
from todo_app.login.oauth_manager import OAuthManager

from todo_app.view_model import ViewModel
from todo_app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    mongo_items = MongoItems(MongoConfig())
    login_manager = LoginManager()
    oauth_manager = OAuthManager(OAuthConfig())

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(oauth_manager.get_authorize_url())

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id, oauth_manager.get_role(user_id))

    login_manager.init_app(app)

    @app.route('/login/callback')
    def login():
        token = oauth_manager.get_token(request.args.get('code'))
        user = oauth_manager.get_user(token)
        login_user(user)
        return redirect('/')

    @app.route('/')
    @login_required
    def index():
        items = sorted(mongo_items.get_items(),
                       key=lambda item: item.status == 'Done')
        item_view_model = ViewModel(items, current_user_can_write())
        return render_template('index.html', view_model=item_view_model)

    @app.route('/items', methods=['POST'])
    @login_required
    @writer_required
    def add_item():
        mongo_items.add_item(request.form.get('new_item'))
        return redirect('/')

    @app.route('/items/<id>/complete', methods=['POST'])
    @login_required
    @writer_required
    def complete_item(id):
        mongo_items.update_status(id, 'Done')
        return redirect('/')

    @app.route('/items/<id>/uncomplete', methods=['POST'])
    @login_required
    @writer_required
    def uncomplete_item(id):
        mongo_items.update_status(id, 'To Do')
        return redirect('/')

    return app
