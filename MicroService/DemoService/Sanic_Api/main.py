# pylint: disable=E0401,E0611
import logging

from sanic import Sanic, response
import json
from app.model import Users
from tortoise.contrib.sanic import register_tortoise
from tortoise.transactions import in_transaction

app = Sanic(__name__)


# @app.route("/")
# async def list_all(request):
#     users = await Users.all()
#     return response.json({"users": [str(user) for user in users]})


@app.route("/")
async def list_all(request):
  async with in_transaction() as conn:
    list_of_dicts = await conn.execute_query_dict(
        "select user_id from users "
    )
    print (list_of_dicts)
  return response.json(list_of_dicts)

register_tortoise(
    app, generate_schemas=False ,
    config = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': 'localhost',
                'port': '5432',
                'user': 'postgres',
                'password': 'Passw0rd_2020',
                'database': '2fast_api',
                'maxsize' : '1000'
            }
        },
    },
    'apps': {
        'models': {
            'models': ['__main__'],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    }
    }
    )


if __name__ == "__main__":
    app.run(port=8000 , debug=True , workers=6 )