from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise



class Status(models.Model):
    status_id = fields.IntField(pk=True)
    status_name = fields.CharField(max_length=80)
    class Meta:
        table="status"
    # def __str__(self):
    #     return  str(self.status_name)
Status_Pydantic  = pydantic_model_creator(Status)
