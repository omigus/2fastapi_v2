from sanic import response , Blueprint
from tortoise.transactions import in_transaction
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.jwt import authorized
from app.api.projects.service import find
from app.models import Projects
from app.utils.json import  UUIDEncoder
import json





project_service = Blueprint(name="project_service")
@project_service.route("/projects" , methods=['GET'])
@authorized()
async def find_all_project(req , current_user):
  Projects_Pydantic =  pydantic_model_creator(Projects)
  result = await Projects_Pydantic.from_queryset(
        Projects.all().prefetch_related(
            "status", 
        ))
  return response.json({"projects": json_data})



@project_service.route("/projects" , methods=['POST'])
@authorized()
async def insert_project(req , current_user):
  return response.json('data')


@project_service.route("/test" , methods=['GET'])
@authorized()
async def list_all(req , current_user):
  async with in_transaction() as conn:
    list_of_dicts = await conn.execute_query_dict(
        "select * from project "
    )
    json_data = json.dumps(list_of_dicts , cls=UUIDEncoder)
  return response.json(json.loads(json_data))

@project_service.route("/2/<id>" , methods=['GET'])
async def test_request_args(req , id):
    return response.json({
        "parsed": True,
        "url": req.url,
        "query_string": req.query_string,
        "args": req.args,
        "query_args": req.query_args,
        "id" : id
    })