from pydantic import BaseModel
import sqlalchemy

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_username", sqlalchemy.String),


)

class User(BaseModel):
    user_username: str

