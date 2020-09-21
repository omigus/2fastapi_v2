import flask
import requests
import os
from app.main.database import InitDB , CloseDB
from datetime import datetime

dt = datetime.now()

def register_token(token , member_public_id):
	try:

			ps_connection  = InitDB()
			if(ps_connection):
				token = str(token)
				member_public_id = str(member_public_id) 
				ps_cursor = ps_connection.cursor()
				query = ("INSERT INTO system_token(system_token , member_public_id , created_on)  VALUES (%s , %s , %s ) ")
				ps_cursor.execute(query, (token ,member_public_id ,dt , ) )
				ps_cursor.close() 
				ps_connection.commit()  
				CloseDB(ps_connection)     
				return 'success'
	except(Exception ) as e:
			print(e)
			return e