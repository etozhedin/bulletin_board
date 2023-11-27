from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY']='secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usr:pw@db:5432/db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
migrate = Migrate(app, db)


from . import models
from . import routes

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)  
