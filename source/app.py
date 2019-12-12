from common import register_error_handlers
from config import Testing as Config
from flask import Flask, jsonify
from flask_restful import Api

from resources.endpoints import Forecast
from resources.endpoints import Register
from resources.endpoints import News

base_uri = f"/api/{(Config.API_VERSION)}"

app = Flask(__name__)
app.config.from_object(Config)
register_error_handlers(app)

api = Api(app)
api.add_resource(Register, f'{base_uri}/register')
api.add_resource(Forecast, f'{base_uri}/forecast')
api.add_resource(News, f'{base_uri}/news')
