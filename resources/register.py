import config

from webargs.flaskparser import use_args
from flask_restful import Resource
from webargs import fields
from flask import url_for
import mysql.connector

from uuid import uuid4
import json
import re

uuidre = re.compile(
    '^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
required_args = {
    'uuid': fields.Str(required=True, validate=lambda uuid: bool(uuidre.match(uuid)))
}

class Register(Resource):
    @use_args(required_args)
    def post(self, args):
        uuid = args['uuid']
        dbconf = config.dbinfo['db']
        reg_table = config.dbinfo['tables']['device_reg_table']

        try:
            cnx = mysql.connector.connect(**dbconf)
            cursor = cnx.cursor(buffered=True)
            
            cursor.execute(f"SELECT * FROM {reg_table} WHERE uuid=\'{uuid}\';")
            first = cursor.fetchone()
            if first is None or len(first[1]) > 0:
                reason = "your device is invalid" if first is None \
                    else "you already have an api key"
                return {"status_code": 400, "reason": reason}

            api_key = str(uuid4())
            cursor.execute(
                f"UPDATE {reg_table} SET api_key=\'{api_key}\' WHERE uuid=\'{uuid}\';")
            cnx.commit()

        except Exception as e:
            print(e)
            return {"status_code": 500, "reason": "internal server error"}

        finally:
            if cnx:
                cnx.close()

        return {"status_code": 200, "reason": "success", "api_key": api_key}
