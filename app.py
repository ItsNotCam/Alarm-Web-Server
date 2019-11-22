from config import Testing as Config
from flask_restful import Api
from flask import Flask
import json
import os

from resources import Forecast
from resources import Register
from resources import News

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instances')
api_version = Config.API_VERSION
base_uri = f"/api/{api_version}"

app = Flask(__name__, instance_path=instance_path)
app.config.from_object(Config)

api = Api(app)
api.add_resource(Register, f'{base_uri}/register')
api.add_resource(Forecast, f'{base_uri}/forecast')
api.add_resource(News, f'{base_uri}/news')
