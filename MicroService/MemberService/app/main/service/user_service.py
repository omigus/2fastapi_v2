import flask
import requests
import os
from app.main.database import InitDB , CloseDB
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid


def findUserNameId(username):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("select count(*) from users where user_username = %s ")
			ps_cursor.execute(query, (username , ) )
			data = ps_cursor.fetchone()
			ps_cursor.close()   
			CloseDB(ps_connection)     
			return data
	except(Exception ) as e:
		return e
def registerUser(username ,password ,company_id):
	hashed_password = generate_password_hash(password, method='sha256')
	user_public_id = str(uuid.uuid4()) 
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("  insert into users( user_public_id , user_username , user_password ,user_is_active,company_id ) values ( %s , %s , %s ,%s ,%s )" )
			ps_cursor.execute(query, (user_public_id,  username , hashed_password , '1', company_id , ) ) 
			ps_connection.commit()
			ps_cursor.close()
			CloseDB(ps_connection)      
			return 'success'
	except Exception as e :
		 return 'error'


	
	