from .projects import *
from .status import *
from tortoise import Tortoise

Tortoise.init_models(["__main__"] ,"app.models" )