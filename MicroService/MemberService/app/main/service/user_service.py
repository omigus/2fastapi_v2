import flask
import requests
import os
from app.main.database import InitDB , CloseDB
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid


def findUserName(username):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("select count(*) from admin where admin_username = %s ")
			ps_cursor.execute(query, (username , ) )
			company = ps_cursor.fetchone()
			ps_cursor.close()   
			CloseDB(ps_connection)     
			return company
	except(Exception ) as e:
		return 'error'
def registerAdmin(username ,password ,company_id):
	hashed_password = generate_password_hash(password, method='sha256')
	admin_public_id = str(uuid.uuid4()) 
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("  insert into admin( admin_public_id , admin_username , admin_password ,admin_is_active,company_id ) values ( %s , %s , %s ,%s ,%s )" )
			ps_cursor.execute(query, (admin_public_id, username , hashed_password , '1', company_id , ) ) 
			ps_connection.commit()
			ps_cursor.close()
			CloseDB(ps_connection)      
			return 'success'
	except Exception as e :
	   return 'error'

	
	