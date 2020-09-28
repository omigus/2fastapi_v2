import flask
import requests
import os
from app.main.database import InitDB , CloseDB
import uuid

def create_project():
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("  insert into project( project_public_id , project_number , project_name ,project_desc,project_startdate ,project_enddate , project_created , project_creator_id , status_id ) values ( %s , %s , %s ,%s ,%s ,%s,%s,%s,%s )" )
			ps_cursor.execute(query, (admin_public_id,  username , hashed_password , '1', company_id , )
			ps_cursor.close()   
			CloseDB(ps_connection)     
			return company
	except(Exception ) as e:
		return 'error'
