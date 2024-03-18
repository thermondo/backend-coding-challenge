from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.users.views import users_bp
from src.core.views import core_bp

from src.users.models import User


app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

# Set up Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "danger"

# Set up bcrypt for the app
bcrypt = Bcrypt(app)

# Set up and migrate DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Registering blueprints
app.register_blueprint(users_bp)
app.register_blueprint(core_bp)


# Callback to reload the user object after login(?)
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
