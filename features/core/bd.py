from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()

def execute_query( sql_query, sql_params={}):
    resultado = db.session.execute(text(sql_query), sql_params).fetchall()
    rows = [row._data for row in resultado]
    return rows