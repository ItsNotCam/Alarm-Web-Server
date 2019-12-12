import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, 'config', 'dbinfo.json')) as file:
    dbinfo = json.loads(file.read())
with open(os.path.join(basedir, 'config', 'forecasts.json')) as file:
    forecasts = json.loads(file.read())
with open(os.path.join(basedir, 'config', 'news.json')) as file:
    news = json.loads(file.read())


class Config(object):
    DEBUG = False
    TESTING = False
    API_VERSION = "v1"


class Testing(Config):
    DEBUG = True
    TESTING = True

    HOST = "127.0.0.1"
    PORT = "5000"
