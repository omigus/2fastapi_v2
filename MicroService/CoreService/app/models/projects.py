from tortoise import fields, models
from .status import Status 

from tortoise import Tortoise
from pydantic import BaseModel
import uuid
import datetime


class Projects(models.Model):
    project_id = fields.IntField(pk=True)
    project_public_id = fields.UUIDField()
    project_number = fields.CharField(max_length=80)
    project_name = fields.CharField(max_length=80)
    project_desc = fields.TextField()
    project_startdate = fields.DatetimeField()
    project_enddate = fields.DatetimeField()
    status = fields.ForeignKeyField('models.Status', related_name='projects')
    project_created = fields.DatetimeField(auto_now=True)
    # project_creator = fields.ForeignKeyField('models.user', related_name='projects')
    class Meta:
        table="project"
        ordering = ["project_id"]
    # def __str__(self):
    #     return  str(self.project_id)+ ',' + str(self.project_public_id) +  ',' + str(self.status) 
    


