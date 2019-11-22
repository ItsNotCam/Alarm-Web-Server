from common.schema import RegisterSchema
import config

from werkzeug.exceptions import *
from webargs.flaskparser import use_args
from flask_restful import Resource
import mysql.connector as conn

from uuid import uuid4


class Register(Resource):
    @use_args(RegisterSchema())
    def post(self, args):
        uuid = args['uuid']
        dbconf = config.dbinfo['db']
        reg_table = config.dbinfo['tables']['device_reg_table']

        cnx = None
        try:
            dbconf['connection_timeout'] = 5
            cnx = conn.connect(**dbconf)
            cursor = cnx.cursor(buffered=True)
            
            cursor.execute(f"SELECT * FROM {reg_table} WHERE uuid=\'{uuid}\';")
            first = cursor.fetchone()
            if first is None or len(first[1]) > 0:
                reason = "your device is invalid" if first is None \
                    else "you already have an api key"
                raise Forbidden(description=reason)

            api_key = str(uuid4())
            cursor.execute(
                f"UPDATE {reg_table} SET api_key=\'{api_key}\' WHERE uuid=\'{uuid}\';")
            cnx.commit()

        except (BadRequest, conn.Error) as exception:
            if isinstance(exception, conn.Error):
                raise InternalServerError("the server encountered a database error")

            raise exception

        finally:
            if cnx is not None:
                cnx.close()

        return {"api_key": api_key}
