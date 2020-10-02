import os
from sanic import Sanic
from simple_bcrypt import Bcrypt
from sanic_cors import CORS, cross_origin
from app.db.db import config as DBconfig
from tortoise.contrib.sanic import register_tortoise
from sanic_limiter import Limiter, get_remote_address



def create_app():
    app = Sanic(__name__)
    bcrypt = Bcrypt(app)
    # CORS(app, automatic_options=True)
    register_tortoise(app, generate_schemas=False ,config = DBconfig)
    limiter = Limiter(app, global_limits=['70 per minute'], key_func=get_remote_address)
    return app