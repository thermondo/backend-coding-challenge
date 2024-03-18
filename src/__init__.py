from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


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

# Set up external integrations
from src.movies.integrations.tmdb import TmdbIntegration  # noqa: E402

tmdb = TmdbIntegration(
    api_key=app.config["TMDB_API_KEY"],
    access_token=app.config["TMDB_ACCESS_TOKEN"],
)

# Registering blueprints
from src.users.views import users_bp  # noqa: E402
from src.core.views import core_bp  # noqa: E402
from src.movies.views import movies_bp  # noqa: E402

app.register_blueprint(users_bp)
app.register_blueprint(core_bp)
app.register_blueprint(movies_bp)


# Callback to reload the user object after login(?)
from src.users.models import User  # noqa: E402


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
