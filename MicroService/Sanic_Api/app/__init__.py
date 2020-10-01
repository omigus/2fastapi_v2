from tortoise import Tortoise, fields, run_async
from tortoise.models import Model

async def run_db():
    await Tortoise.init(
        {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "host": "localhost",
                        "port": "5432",
                        "user": "postgres",
                        "password": "Passw0rd_2020",
                        "database": "2fast_api",
                    },
                }
            },
            "apps": {"models": {"models": ["__main__"], "default_connection": "default"}},
        },
        _create_db=False,
    )
    await Tortoise.generate_schemas()
