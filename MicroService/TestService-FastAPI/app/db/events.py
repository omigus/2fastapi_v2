from typing import List

import databases
import sqlalchemy

DATABASE_URL = "postgresql://postgres:Passw0rd_2020@localhost:5432/2fast_api"
database = databases.Database(DATABASE_URL)

def connect_db():
  return database

async def init_db():
  await database.connect()

async def close_db():
  await database.disconnect()