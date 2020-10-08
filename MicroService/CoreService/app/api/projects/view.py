from sanic import response , Blueprint
from tortoise.transactions import in_transaction
from app.utils.jwt import authorized
from app.api.projects.service import find , insert
from app.models import Projects
from app.utils.json import  UUIDEncoder
from tortoise.exceptions import TransactionManagementError
from app.utils.validate_response import  response_json ,check_content_type , check_json_key 
import json




project_service = Blueprint(name="project_service")
@project_service.route("/projects" , methods=['POST'])
@authorized()
async def insert_project(req , current_user):
  admin_id = int(current_user["admin_id"])
  content_type = await check_content_type(req)
  if content_type != None : 
    return content_type
  compare_key = ['project_number' , 'project_name' , 'project_desc' , 'project_startdate','project_enddate' ,'project_creator_id' , 'status_id']
  check_key = await check_json_key(req,compare_key)
  if check_key != None:
    return check_key
  try:
    result = await insert(req , admin_id)
    return await response_json(result)
  except  Exception as e : 
    return await response_json({
      "status" : "Failed" ,
      "message" : e.message,
      "status_code" : 500
    })

# @project_service.route("/projects" , methods=['GET'])
# @authorized()
# async def fimd

  #   json_data = json.dumps(list_of_dicts , cls=UUIDEncoder)
  # return response.json(json.loads(json_data))



  

