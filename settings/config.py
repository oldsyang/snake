import configparser
import os

from .base import *

config_dir = HERE / 'config.ini'
config = configparser.ConfigParser()
config.read(config_dir)

SITE_HOST = os.getenv('SITE_HOST', config.get('global', 'host', fallback=SITE_HOST))
WEB_PORT = int(os.getenv('WEB_PORT', config.get('global', 'web_port', fallback=WEB_PORT)))

DB_MODE = os.getenv('DB_MODE', config.get('database', 'db_mode', fallback='sqlite'))
if DB_MODE == 'mysql':
    DB_HOST = os.getenv('DB_HOST', config.get('database', 'host', fallback='localhost'))
    DB_USERNAME = os.getenv('DB_USERNAME', config.get('database', 'username', fallback=''))
    DB_PWD = os.getenv('DB_PWD', config.get('database', 'password', fallback=''))
    DB_PORT = os.getenv('DB_PORT', config.get('database', 'port', fallback=3306))
    DB_NAME = os.getenv('DB_NAME', config.get('database', 'db', fallback=''))
    DB_CHARSET = os.getenv('DB_CHARSET', config.get('database', 'charset', fallback='ut8mb4'))
    DB_TABLE_PREFIX = os.getenv('DB_TABLE_PREFIX', config.get('database', 'prefix', fallback=''))
    DB_URL = f'mysql+pymysql://{DB_USERNAME}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}'

else:
    DB_URL = os.getenv('DB_URL', config.get('database', 'db_url', fallback=''))

if os.path.isfile(HERE / 'settings/private.py'):
    from .private import *

    if DB_MODE == 'mysql':
        DB_URL = f'mysql+pymysql://{DB_USERNAME}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}'

