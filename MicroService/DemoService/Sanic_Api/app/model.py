from tortoise.models import Model
from tortoise import fields

class Users(Model):
    user_id = fields.IntField(pk=True)
    user_username = fields.TextField()
    user_password = fields.TextField()

    def __str__(self):
        return self.user_username +  self.user_password