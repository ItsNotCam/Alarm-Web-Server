from werkzeug.exceptions import Unauthorized, InternalServerError, FailedDependency
from webargs.flaskparser import use_args
from common.schema import NewsSchema
from flask_restful import Resource
from flask import jsonify
from resources import authorize

import config
import requests

# TODO: implement news grabbing from The Washington Post
class News(Resource):
    @use_args(NewsSchema())
    def get(self, args):
        authorize(args['uuid'], args['api_key'])

        news_type = args['news_type']
        url = f"https://api.nytimes.com/svc/topstories/v2/{news_type}.json"
        try:
            response = requests.get(
                url=url,
                params={"api-key": config.news['api_key']}
            ).json()

            if response is None or 'status' not in response or response['status'] != "OK":
                raise FailedDependency("failed to retrieve news from offsite api")

            return jsonify({"news": response['results']})

        except (FailedDependency, requests.exceptions.RequestException) as exception:
            if isinstance(exception, FailedDependency):
                raise exception

        raise InternalServerError()
        