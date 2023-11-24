from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY']='secret_key'
app.config['SQLALCHEMY_DB']='sqlite:///db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from . import models
from . import routes

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)  