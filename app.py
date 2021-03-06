
import sqlite3
from flask import Flask, session
from werkzeug.security import safe_str_cmp
from flask_cors import CORS
from os import getenv 
from dotenv import load_dotenv
from functools import wraps
from datetime import timedelta


from blueprints.rank import rank
from blueprints.mos import mos
from blueprints.position_title import position_title
from blueprints.year import year
from blueprints.officer import officer
from blueprints.assignment import assignment
from blueprints.user import user
from blueprints.position_title_join import position_title_join

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = getenv('SECRET_KEY', None)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=1)
# app.config['SESSION_COOKIE_SAMESITE'] = "None"
# app.config['CORS_HEADERS'] = ['SET_COOKIE']

# app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['SESSION_COOKIE_SAMESITE'] = "None"

# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='None',
# )
app.register_blueprint(rank)
app.register_blueprint(mos)
app.register_blueprint(position_title)
app.register_blueprint(year)
app.register_blueprint(officer)
app.register_blueprint(assignment)
app.register_blueprint(user)
app.register_blueprint(position_title_join)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
