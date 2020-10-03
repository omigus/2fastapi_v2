from tortoise.transactions import in_transaction
from app.models import Projects

async def insert(data):
  projects = await Projects.create(name="New User")
  return response.json({"users": [str(user) for user in projects]})

async def find():
    Project = await Projects.all().prefetch_related(
            "status", 
        )
    # Project = await Projects_Pydantic.from_queryset(await Projects.all().prefetch_related(
    #         "status", 
    #     ))
    return Project