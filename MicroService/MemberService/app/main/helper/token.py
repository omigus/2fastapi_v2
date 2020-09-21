
from functools import wraps
from flask import Flask, request, jsonify, make_response, Blueprint
import uuid 
import jwt
import json
from functools import wraps
import urllib 
import os
import requests
from app.main.database import InitDB , CloseDB


def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if "Authorization" in request.headers:
			token = request.headers["Authorization"]

		if not token:
			return jsonify({"message": "Token is missing!"}), 401

		
		access_token = token.split(" ")[1]

		try:
			data = jwt.decode(access_token, os.getenv('SECRET_KEY'))
			current_user = data
		except Exception as e:
			return jsonify({"message": "Invalid Token"}), 401

		return f(current_user, *args, **kwargs)

	return decorated


def token_required_admin(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if "Authorization" in request.headers:
			token = request.headers["Authorization"]

		if not token:
			return jsonify({"message": "Token is missing!"}), 401

		
		access_token = token.split(" ")[1]
		
		try:
			data = jwt.decode(access_token, os.getenv('SECRET_KEY'))
			member_public_id = data["member_public_id"]
			ps_connection  = InitDB()
			if(ps_connection):
				ps_cursor = ps_connection.cursor()
				query = ("select system_token from system_token "
					   " where member_public_id = %s "
					   " order by system_token_id desc " 
					   " limit 1" )
				ps_cursor.execute(query, ( member_public_id , ) )
				rv = ps_cursor.fetchone()
				ps_cursor.close()
				CloseDB(ps_connection) 
				activeToken = rv[0]
			
				if activeToken != access_token :
					return jsonify({"message": "Token BlackList"}), 401
				current_user = data
		except Exception as e:
			print (e)
			return jsonify({"message": "Invalid Token"}), 401

		return f(current_user, *args, **kwargs)

	return decorated
