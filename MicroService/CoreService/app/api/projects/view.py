from sanic import response , Blueprint
from tortoise.transactions import in_transaction
from app.utils.jwt import authorized
from app.api.projects.service import find
from app.models import Projects
from app.utils.json import  UUIDEncoder
from app.utils.validate_response import  response_json ,check_content_type , check_json_key 
import json

project_service = Blueprint(name="project_service")
@project_service.route("/projects" , methods=['GET'])
@authorized()
async def insert_project(req , current_user):
    content_type = await check_content_type(req)
    if content_type != None : 
      return content_type
    compare_key = ['a' , 'b']
    check_key = await check_json_key(req,compare_key)
    if check_key != None:
      return check_key
    async with in_transaction() as conn:
      list_of_dicts = await conn.execute_query_dict(
          "select * from users "
      )
      json_data = json.dumps(list_of_dicts , cls=UUIDEncoder)
    return response.json(json.loads(json_data))
    

