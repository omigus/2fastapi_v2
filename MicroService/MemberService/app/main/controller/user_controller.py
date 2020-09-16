from flask import Blueprint , jsonify ,request
import json
import psycopg2
from app.main.service.company_service import findByPublic ,check_exists_company_users_current , checkcompany_admin_limit
from app.main.service.user_service import findUserName ,registerAdmin
from app.main.helper.token import token_required
import datetime

UserService = Blueprint("UserService", __name__,url_prefix= "/api/v2")

@UserService.route("/member/admin", methods=["POST"])
@token_required
def Register_admin_company(current_user):
    if request.content_type != 'application/json':
        return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
    params = request.get_json()  
    if "company_public_id" not in params.keys():
        return jsonify({"status": "failed", "message": "Invalid company_public_id" }), 404
    if "admin_username" not in params.keys():
        return jsonify({"status": "failed", "message": "Invalid admin_username" }), 404
    if "admin_password" not in params.keys():
        return jsonify({"status": "failed", "message": "Invalid admin_password" }), 404
    company = findByPublic(params["company_public_id"])
    if company == "error":
        return jsonify({"status": "failed", "message": "company_public_id is invalid in db" }), 404
    username = findUserName(params["admin_username"])
    if username == "error":
        return jsonify({"status": "failed", "message": "Error" }), 500
    if username[0] > 0 :
        return jsonify({"status": "failed", "message": "Username already registered" }), 409 
    admin_create_limit =  checkcompany_admin_limit(params["company_public_id"])
    ##เหลือเช็คว่า ตอนนี้มียูซเซอร์ปัจจุบันแล้วกี่คน adminCreate_limit จะคืนค่าสูงสุดที่สร้างได้มาให้
  
    if username[0] == 0 :
        regis_admin = registerAdmin(params["admin_username"] ,params["admin_password"] ,company[0]  )
        if regis_admin == 'success':
            return jsonify({"status": "failed", "message": "isexist"}), 200
   
        # jsonify(company)
    #     company_name = params["company_name"]
    #     uuid_entry = str(uuid.uuid4()) 
    #     ps_connection  = InitDB()
    #     if(ps_connection):
    #         ps_cursor = ps_connection.cursor()
    #         query = ("  insert into company( company_name , company_public_id , company_is_active ,created_on ) values ( %s , %s , %s ,%s )" )
    #         ps_cursor.execute(query, (company_name, uuid_entry , '1', datetime.datetime.now() ) )
    #         ps_connection.commit()
    #         ps_cursor.close()
    #         CloseDB(ps_connection)      
    #         token = request.headers["Authorization"]
    #         access_token = token.split(" ")[1]
    #         status_code  = create_storage(access_token ,uuid_entry ) 
    #         if int (status_code) == 201 :   
    #             return jsonify({"status" : 'success' , "company_public_id" : uuid_entry } ),201

