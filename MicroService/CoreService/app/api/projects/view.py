from sanic import response , Blueprint
from tortoise.transactions import in_transaction
from tortoise.contrib.pydantic import pydantic_model_creator
from app.utils.jwt import authorized
from app.api.projects.service import find
from app.models import Projects



project_service = Blueprint(name="project_service")


@project_service.route("/projects" , methods=['GET'])
@authorized()
async def find_all_project(req , current_user):
  projects = await find()
  Projects_Pydantic = pydantic_model_creator(Projects)
  tourpy = await Projects_Pydantic.from_tortoise_orm(projects)
  return response.json({"projects": tourpy.json()})
  # return response.json({"projects": [str(project) for project in projects]})


@project_service.route("/projects" , methods=['POST'])
@authorized()
async def insert_project(req , current_user):
  return response.json('data')


@project_service.route("/test" , methods=['GET'])
@authorized()
async def list_all(req , current_user):
  async with in_transaction() as conn:
    list_of_dicts = await conn.execute_query_dict(
        "select user_id from users "
    )
  return response.json(current_user)

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