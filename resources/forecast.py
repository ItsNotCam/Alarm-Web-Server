import config

from webargs.flaskparser import use_args
from flask_restful import Resource
from webargs import fields
import requests
import re

forecast_types = config.forecasts['forecast_types']
headers = config.forecasts['headers']
urls = config.forecasts['urls']

api_key_re = re.compile(
    '^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
required_args = {
    'forecast_type': fields.Str(required=True, validate=lambda ft: ft in forecast_types),
    'country_code': fields.Str(required=True, validate=lambda cc: re.fullmatch("[A-Za-z]{2}", cc)),
    'api_key': fields.Str(required=True, validate=lambda apik: bool(api_key_re.match(apik))),
    'units': fields.Str(required=True, validate=lambda u: u in ["imperial", "metric"]),
    'city': fields.Str(required=True, validate=lambda city: re.fullmatch("[A-Za-z]{3,}", city)),
    'tts': fields.Bool(required=False)
}


class Forecast(Resource):
    @use_args(required_args)
    def get(self, args):
        # TODO: VALIDATE API KEY
        # TODO: ADD CACHING
        forecast_type = args['forecast_type']
        city = "%s,%s" % (args['city'], args['country_code'])
        weather = requests.get(
            url=urls[forecast_type],
            headers=headers,
            params={'q': city, 'units': args['units']}
        ).json()

        # TODO: IMPLEMENT WPL
        # TODO: IMPLEMENT TEXT-TO-SPEECH
        return {"forecast": weather}
