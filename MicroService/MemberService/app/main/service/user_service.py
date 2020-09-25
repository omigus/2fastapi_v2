import flask
import requests
import os
from app.main.database import InitDB , CloseDB
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from psycopg2.extras import RealDictCursor

def find_all_user(company_id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor(cursor_factory=RealDictCursor)
			sql = (" select users.company_id , users.user_is_active , users.user_public_id , users.user_username , userdetails.userdetails_firstname , userdetails.userdetails_lastname , userdetails.userdetails_employee_id ,   userdetails.userdetails_avatar  from users  "
					" left join userdetails on users.user_id = userdetails.user_id "
          			" where company_id = %s ")
			ps_cursor.execute(sql, (company_id , ) ) 
			data = ps_cursor.fetchall()
			ps_cursor.close()
			CloseDB(ps_connection)      
			return ['success' , data ,200]
	except Exception as e :
		return ['success' ,'failed ' +e.message  ,500]
    

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

def findUserIdfromPublic_id(user_public_id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("select user_id from users where user_public_id = %s ")
			ps_cursor.execute(query, (user_public_id , ) )
			data = ps_cursor.fetchone()
			ps_cursor.close()   
			CloseDB(ps_connection)    
			return data[0]
	except(Exception ) as e:
		return e

def findValidUserId(user_public_id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("select count(*) from users where user_public_id = %s ")
			ps_cursor.execute(query, (user_public_id , ) )
			data = ps_cursor.fetchone()
			ps_cursor.close()   
			CloseDB(ps_connection)    
			count = int(data[0]) 
			return (count)
	except(Exception ) as e:
		return e

def findValidUserId_details(user_public_id):
	try:
		user_id = findUserIdfromPublic_id(user_public_id)
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("select count(*) from userdetails where user_id = %s ")
			ps_cursor.execute(query, (user_id , ) )
			data = ps_cursor.fetchone()
			ps_cursor.close()   
			CloseDB(ps_connection)    
			count = int(data[0]) 
			return (count)
	except(Exception ) as e:
		return e


def insertUser_details(params,user_public_id):
	try:
		user_id = findUserIdfromPublic_id(user_public_id)
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("  insert into userdetails( userdetails_employee_id , userdetails_firstname , userdetails_lastname , userdetails_phone , userdetails_email , userdetails_position ,user_id ) values ( %s , %s , %s ,%s ,%s ,%s ,%s) " )
			ps_cursor.execute(query, (params["userdetails_employee_id"] , params["userdetails_firstname"] , params["userdetails_lastname"] ,params["userdetails_phone"],params["userdetails_email"] , params["userdetails_position"] ,user_id , ) ) 
			ps_connection.commit()
			ps_cursor.close()
			CloseDB(ps_connection)      
			return 'success'
	except Exception as e :
		print(e)
		return e

def update_userdetails(params,user_public_id):
	try:
		column = ''
		for column_name in params.keys():
			column = str(column) + str(column_name + " = '" + params[column_name] + "' ,")
		sql_prepare = (column[0:(len(column))-1])
		user_id = findUserIdfromPublic_id(user_public_id)
		sql_builder = "UPDATE userdetails SET "  + str( sql_prepare) + " WHERE user_id = %s "
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			ps_cursor.execute(sql_builder, (user_id , ) ) 
			ps_connection.commit()
			ps_cursor.close()
			CloseDB(ps_connection)      
			return ['success' ,'Edited : ' +str (user_public_id)  ,200]
	except Exception as e :
		return ['success' ,'failed ' +e.message  ,500]
