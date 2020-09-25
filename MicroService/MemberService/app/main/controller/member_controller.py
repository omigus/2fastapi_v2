from flask import Blueprint , jsonify ,request
import json
import psycopg2
from app.main.service.company_service import *
from app.main.service.admin_service import findAdminNameId ,registerAdmin
from app.main.service.user_service import *
from app.main.helper.token import token_required , token_required_admin
import datetime 

MemberService = Blueprint("MemberService", __name__,url_prefix= "/api/v2")

@MemberService.route("/member/admin", methods=["POST"])
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
    user_id = findAdminNameId(params["admin_username"])
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



@MemberService.route("/member/user", methods=["POST"])
@token_required_admin
def Register_user_company(current_user):
    if request.content_type != 'application/json':
        return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
    params = request.get_json()  
    if "company_public_id" not in params.keys():
        return jsonify({"status": "failed", "message": "Invalid company_public_id" }), 404
    if "user_username" not in params.keys():
        return jsonify({"status": "failed", "message": "Invalid user_username" }), 404
    if "user_password" not in params.keys():
        return jsonify({"status": "failed", "message": "Invalid user_password" }), 404
    company_id = findIdByPublic_company(params["company_public_id"])
    if company_id == "error":
        return jsonify({"status": "failed", "message": "company_public_id is invalid in db" }), 404
    user_id = findUserNameId(params["user_username"])
    if user_id == "error":
        return jsonify({"status": "failed", "message": "Error" }), 500
    if user_id[0] > 0 :
        return jsonify({"status": "failed", "message": "Username already registered" }), 409 
    try :
        user_create_limit =  checkcompany_user_limit(params["company_public_id"])
        
        user_current_active = checkcompany_current_user_active(company_id , 1)

        if user_current_active >= user_create_limit :
            return jsonify({"status": "failed", "message": "over limit users_create_limit"  , "user_current_active" : user_current_active , "user_create_limit"  : user_create_limit}), 200 
        if user_current_active <= user_create_limit:
            if user_id[0] == 0 :
                regis_user = registerUser(params["user_username"] ,params["user_password"] ,company_id  )
                if regis_user == 'success':
                    return jsonify({"status": "success", "username" :params["user_username"] }), 200
    except Exception as e :
        return jsonify({"status": "Failed" , "message" : "failed company invalid or did not have group all" }), 500




@MemberService.route("/userdetails/<user_public_id>", methods=["POST"])
@token_required_admin
def insert_userdetails(current_user , user_public_id):
    if request.content_type != 'application/json':
        return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
    params = request.get_json()  
    valid_user = findValidUserId(user_public_id)
    if valid_user != 1 :
        return jsonify({"status": "Failed" , "message" : "Invalid User" }), 400
    valid_user_details = findValidUserId_details(user_public_id)
    if valid_user_details >= 1 :
        return jsonify({"status": "Failed" , "message" : " Already has UserDetails" }), 400
    result = insertUser_details(params,user_public_id)
    if result == 'success':
        return jsonify({"status": "success", "user_public_id" : user_public_id }), 201
    else:
        return jsonify({"status": "Failed" , "message" :'server error' }), 500

@MemberService.route("/userdetails/<user_public_id>", methods=["PATCH"])
@token_required_admin
def update_userdetail(current_user , user_public_id):
    if request.content_type != 'application/json':
        return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
    params = request.get_json()  
    valid_user = findValidUserId(user_public_id)
    if valid_user != 1 :
        return jsonify({"status": "Failed" , "message" : "Invalid User" }), 400
    valid_user_details = findValidUserId_details(user_public_id)
    result = update_userdetails(params,user_public_id)
    return jsonify({"status": result[0], "message" : result[1] }), result[2]
   