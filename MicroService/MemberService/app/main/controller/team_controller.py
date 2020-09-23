from flask import Blueprint , jsonify ,request
import json
import psycopg2
from app.main.helper.token import token_required , token_required_admin
from app.main.service.team_service import *

TeamService = Blueprint("TeamService", __name__,url_prefix= "/api/v2")



@TeamService.route("/team", methods=["GET"])
@token_required_admin
def display_team_companyId(current_user):
	company_id = current_user['company_id']
	if request.content_type != 'application/json':
		return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
	result = findAll_Company_admin(company_id)
	return jsonify ({"status": result[0], "message": result[1] }), result[2]


@TeamService.route("/team/<id>", methods=["GET"])
@token_required_admin
def display_team_company_by_id(current_user , id):
	company_id = current_user['company_id']
	if request.content_type != 'application/json':
		return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
	result = findTeam_ById(id)
	return jsonify ({"status": result[0], "message": result[1] }), result[2]

@TeamService.route("/team/<id>/dashboard", methods=["GET"])
@token_required_admin
def dashboard_company_by_id(current_user , id):
	company_id = current_user['company_id']
	if request.content_type != 'application/json':
		return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
	team_member = findteamMember_details(id)
	team = findTeam_ById(id)
	return jsonify ({ "team_member"  :team_member[1] , "team": team[1]  }), 200

@TeamService.route("/team", methods=["POST"])
@token_required_admin
def Register_team_company(current_user):
	company_id = current_user['company_id']
	admin_id = current_user['admin_id']
	if request.content_type != 'application/json':
		return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
	params = request.get_json()  
	if "team_name" not in params.keys():
		return jsonify({"status": "failed", "message": "Invalid team_name" }), 404
	
	result = InsertTeam(params["team_name"] , '-' , admin_id , company_id)
	if result == 'success':
		return jsonify ({"status": "success", "message": "team created" }), 201
	else :
		jsonify({"status": "failed", "message": "error" }), 500


@TeamService.route("/team/member", methods=["POST"])
@token_required_admin
def Register_team_member_company(current_user):
	company_id = current_user['company_id']
	admin_id = current_user['admin_id']
	if request.content_type != 'application/json':
		return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
	params = request.get_json()  
	if "user_id" not in params.keys():
		return jsonify({"status": "failed", "message": "Invalid user_id" }), 404
	if "team_id" not in params.keys():
		return jsonify({"status": "failed", "message": "Invalid team_id" }), 404
	result = InsertTeamMember(params["team_id"] , params["user_id"] )
	if result != 'success':
		return jsonify ({"status": result[0], "message": result[1] }), result[2]
	else:
		return jsonify ({"status": "success", "message": "success"  , "team_id" : params["team_id"] , "user_id " : params["user_id"] }), 200


@TeamService.route("/team/member", methods=["DELETE"])
@token_required_admin
def Remove_team_member_company(current_user):
	company_id = current_user['company_id']
	admin_id = current_user['admin_id']
	if request.content_type != 'application/json':
		return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
	params = request.get_json()  
	if "user_id" not in params.keys():
		return jsonify({"status": "failed", "message": "Invalid user_id" }), 404
	if "team_id" not in params.keys():
		return jsonify({"status": "failed", "message": "Invalid team_id" }), 404
	result = RemoveTeamMember(params["team_id"] , params["user_id"] )
	if result == 'success':
		return jsonify ({"status": "success", "message": "removed" }), 404
	else :
		jsonify({"status": "failed", "message": "invalid fk key" }), 500