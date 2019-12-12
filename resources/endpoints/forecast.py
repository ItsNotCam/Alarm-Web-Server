from resources.wpl import FiveDayForecast, Forecast
from resources.endpoints import authorize
from resources import tts

from common.schema import ForecastSchema
import config

from werkzeug.exceptions import InternalServerError, BadRequest, FailedDependency
from webargs.flaskparser import use_args, parser, abort
from flask_restful import Resource

from datetime import datetime, timedelta
import requests, json

headers = config.forecasts['headers']
urls = config.forecasts['urls']

class Forecast(Resource):
    @use_args(ForecastSchema())
    def get(self, args):
        # authorize(args['uuid'], args['api_key'])

        # TODO: ADD CACHING
        forecast_type = args['forecast_type']
        city = "%s,%s" % (args['city'], args['country_code'])
        headers = config.forecasts['headers']
        try:
            weather = requests.get(
                url=urls[forecast_type],
                headers=headers,
                params={'q': city, 'units': args['units']}
            ).json()

            if False in [c.isdigit() for c in weather['cod']]:
                raise FailedDependency("invalid status code retrieved from offsite api")

            code = int(weather['cod'])
            if weather is None or code != 200:
                message = "failed to retrieve forecast from offsite api"
                if weather is not None:
                    message += " - code:%d - %s" % (code, str(weather['message']))
                
                raise FailedDependency(message)

        except (FailedDependency, requests.exceptions.RequestException) as exception:
            if isinstance(exception, FailedDependency):
                raise exception

            raise FailedDependency("failed to retrieve forecast from offsite api")
        
        if 'tts' in args:
            # fix this to implement forecast types
            try:
                text = tts.tts(
                    {"forecast":weather}, 
                    datetime.today() + timedelta(days=1)
                )  

                return {
                    "tts": text,
                    "forecast": weather
                }

            # TODO: implement more specific error handling
            except Exception as e:
                print(e)
                raise InternalServerError()

        return {"forecast": weather}
