from os import getenv
from dotenv import load_dotenv
import pathlib

load_dotenv(str(pathlib.Path(__file__).parent.resolve()) + '/.env')

DATABASE_URI = getenv('DATABASE_URI', 'postgresql://admin:admin@localhost:5434/movie')
TEST_DATABASE_URI = getenv('TEST_DATABASE_URI')
DEFAULT_DATABASE_URI = getenv('DEFAULT_DATABASE_URI')

REDIS_URL = getenv('REDIS_URL', 'redis://localhost:6379/0')

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


ACTIVATION_CODE_SEP = getenv('ACTIVATION_CODE_SEP')
