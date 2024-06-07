from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from sqlalchemy.orm import relationship

db = SQLAlchemy()


def create_app(db_var):
    #abs_instance_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'instance')) #<--- this will be the instance directory
    #, instance_path=abs_instance_path
    app = Flask(__name__, template_folder = "templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_var
    app.secret_key = 'cms'

    #db.init_app(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models.user import User


    @login_manager.user_loader
    def load_user(pid):
        return User.query.get(pid)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for("index"))

    bcrypt = Bcrypt(app)


    from .routes.routes import start
    start(app, db, bcrypt)

    migrate = Migrate(app, db)


    return app
