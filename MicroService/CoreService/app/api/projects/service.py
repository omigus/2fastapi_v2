from tortoise.transactions import in_transaction
from app.models import Projects
import datetime, pytz
from app.utils.validate_response import  response_json
import uuid
tz = pytz.timezone('Asia/Bangkok')

async def insert(req , admin_id):
  params = req.json 
  project_startdate = datetime.datetime.fromtimestamp(int(params["project_startdate"]))
  project_enddate = datetime.datetime.fromtimestamp(int(params["project_enddate"]))
  async with in_transaction() as conn:
    dt = datetime.datetime.now(tz)
    uuid_entry = str( uuid.uuid4() ) 
    insert_statement = await conn.execute_query(
        " insert into project( project_public_id ,project_number , project_name , project_desc , project_startdate,project_enddate , project_created , project_creator_id , status_id ) "
        " VALUES ( $1 , $2 , $3 ,$4 ,$5 , $6 , $7 , $8 , $9) "  , 
        [ uuid_entry , params["project_number"], params["project_name"]  , params["project_desc"]  , project_startdate  , project_enddate  , dt, admin_id , params["status_id"]]
      )
    return ({
      "status" : "Success" ,
      "message" :  { "project_public_id" :  uuid_entry  , "project_number" : params["project_number"] } , 
      "status_code" : 201
    })
    


async def find():
    Project = await Projects.all().prefetch_related(
            "status", 
        )
    return Project