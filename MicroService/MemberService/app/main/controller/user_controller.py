from flask import Blueprint , jsonify ,request
import json
import psycopg2
from app.main.service.company_service import findByPublic_company ,check_exists_company_users_current , checkcompany_admin_limit ,checkcompany_current_admin_active ,findIdByPublic_company
from app.main.service.user_service import findUserNameId ,registerAdmin
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
    company_id = findIdByPublic_company(params["company_public_id"])
    if company_id == "error":
        return jsonify({"status": "failed", "message": "company_public_id is invalid in db" }), 404
    user_id = findUserNameId(params["admin_username"])
    if user_id == "error":
        return jsonify({"status": "failed", "message": "Error" }), 500
    if user_id[0] > 0 :
        return jsonify({"status": "failed", "message": "Username already registered" }), 409 
    try :
        admin_create_limit =  checkcompany_admin_limit(params["company_public_id"])
        admin_current_active = checkcompany_current_admin_active(company_id , 1)
        if admin_current_active >= admin_create_limit :
            return jsonify({"status": "failed", "message": "over limit admin_create_limit"  , "admin_current_active" : admin_current_active , "admin_create_limit"  : admin_create_limit}), 200 
        if admin_current_active <= admin_create_limit:
            if user_id[0] == 0 :
                regis_admin = registerAdmin(params["admin_username"] ,params["admin_password"] ,company_id  )
                if regis_admin == 'success':
                    return jsonify({"status": "success", "username" :params["admin_username"] }), 200
    except Exception as e :
        return jsonify({"status": "Failed" , "message" : "failed company invalid or did not have group all" }), 500



# @UserService.route("/member/user", methods=["POST"])
# @token_required
# def Register_user_company(current_user):
#     if request.content_type != 'application/json':
#         return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
#     params = request.get_json()  
#     except Exception as e :
#         return jsonify({"status": "Failed" , "message" : "failed company invalid or did not have group all" }), 500
     