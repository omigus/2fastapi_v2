from sanic import response , Blueprint
from tortoise.transactions import in_transaction
from app.utils.jwt import authorized


project_service = Blueprint('project_service')

def json(body, status=200, headers=None):
    return HTTPResponse(json_dumps(body), headers=headers, status=status,
    content_type="application/json")

@project_service.route("/test" , methods=['GET'])
@authorized()
async def list_all(req , current_user):
  async with in_transaction() as conn:
    list_of_dicts = await conn.execute_query_dict(
        "select user_id from users "
    )
    print (list_of_dicts[0])
    print(current_user)
  return response.json(list_of_dicts[0])

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