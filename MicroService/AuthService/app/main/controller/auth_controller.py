from flask import Blueprint , jsonify ,request
import json
from werkzeug.security import check_password_hash
import jwt
import psycopg2
from app.main.database import InitDB , CloseDB
from app.main.helper.token import token_required
from app.main.service.auth_service import register_token
import datetime
import os

AuthService = Blueprint("AuthService", __name__,url_prefix= "/api/v2")

@AuthService.route("/login/admin", methods=["POST"])
def login_admin():
	params = request.get_json()
	if request.content_type != 'application/json':
		return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
	if not params or not params['username'] or not params['password']:
		return jsonify({ "status" : "failed" , 'message' : "Username or password is empty " }  ) , 401
	username = params["username"]
	password = params["password"]
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = (" SELECT * FROM admin where admin_username = %s " )
			ps_cursor.execute(query, ( username , ) )
			rv = ps_cursor.fetchone()
			ps_cursor.close()
			CloseDB(ps_connection) 
			if not rv :
				return jsonify({"status": "failed", 'message': "Username is incorrect "}), 401  
			password = rv[5]
			public_id = rv[1]
			user_id = rv[0]
			if check_password_hash(password , params['password']):
				token = jwt.encode({'member_public_id' : str(public_id),'admin_id' : str(user_id) ,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv('EXPIRED')))}, os.getenv('SECRET_KEY'))
				token = token.decode('UTF-8')
				result = register_token(token ,public_id )
				if result == 'success': 
					return jsonify({'token':token}), 200
				else:
					return jsonify({"status": "failed", 'message': "... "}), 500
			else :
				return jsonify({"status": "failed", 'message': "Password is incorrect "}), 401
	except Exception as e :
		return e

@AuthService.route("/test", methods=["POST"])
@token_required
def test(current_user):
	return jsonify(current_user)
	