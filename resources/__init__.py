from werkzeug.exceptions import Unauthorized, InternalServerError
import mysql.connector as conn
import config

def authorize(uuid, api_key):
    reg_table = config.dbinfo['tables']['device_reg_table']
    dbinfo = config.dbinfo['db']

    cnx = None
    try:
        dbinfo['connection_timeout'] = 5
        cnx = conn.connect(**dbinfo)
        cursor = cnx.cursor()
        cursor.execute(f"SELECT * FROM {reg_table} WHERE uuid=\'{uuid}\' AND api_key=\'{api_key}\';")
        if cursor.fetchone() is not None:
            return True
    
    except conn.Error as exception:
        message = "database offline" if 'lost connection' in exception.msg.lower() \
            else "database error"
        raise InternalServerError(message)
    
    finally:
        if cnx is not None:
            cnx.close()
    
    raise Unauthorized("invalid credentials")

from .forecast import Forecast
from .register import Register
from .news import News