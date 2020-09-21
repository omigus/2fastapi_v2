import flask
import requests
import os
from app.main.database import InitDB , CloseDB
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime
import uuid

dt = datetime.now()

### ต้องมาทำต่อ ####
### เหลือ หา team ทั้หงมดและ กับ หา ID เดียว
# def findAll():
# 	try:
# 		ps_connection  = InitDB()
# 		if(ps_connection):
# 			ps_cursor = ps_connection.cursor()
# 			query = (" select * from team left join team_has_users on team.team_id = team_has_users.team_id where "
# 							 " team.team_id = %s "
# 			 )
# 			ps_cursor.execute(query, (team_id ) ) 
# 			team = ps_cursor.fetchone()
# 			ps_cursor.close()
# 			CloseDB(ps_connection)      
# 			return team
# 	except Exception as e :
# 		return 'error'

# def findTeambyId(id):
# 	try:
# 		ps_connection  = InitDB()
# 		if(ps_connection):
# 			ps_cursor = ps_connection.cursor()
# 			query = (" select * from team left join team_has_users on team.team_id = team_has_users.team_id where "
# 							 " team.team_id = %s "
# 			 )
# 			ps_cursor.execute(query, (team_id ) ) 
# 			team = ps_cursor.fetchone()
# 			ps_cursor.close()
# 			CloseDB(ps_connection)      
# 			return team
# 	except Exception as e :
# 		return 'error'


def InsertTeam(team_name , team_avatar , admin_id , company_id):
	team_uuid = str(uuid.uuid4()) 
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("  insert into team ( team_public_id , team_name , team_avatar ,team_is_active,created_on , admin_id , company_id ) values ( %s , %s , %s ,%s ,%s ,%s ,%s )" )
			ps_cursor.execute(query, (team_uuid,  team_name , team_avatar , '1', dt  , admin_id ,company_id ) ) 
			ps_connection.commit()
			ps_cursor.close()
			CloseDB(ps_connection)      
			return 'success'
	except Exception as e :
		 return 'error'


def InsertTeamMember(team_id , user_id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("  insert into team_has_users ( team_id ,user_id ) values ( %s , %s )" )
			ps_cursor.execute(query, (team_id , user_id, ) ) 
			ps_connection.commit()
			ps_cursor.close()
			CloseDB(ps_connection)      
			return 'success'
	except Exception as e :
		 return 'error'

def RemoveTeamMember(team_id , user_id) :
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("  delete from team_has_users where team_id = %s and user_id = %s " )
			ps_cursor.execute(query, (team_id , user_id, ) ) 
			ps_connection.commit()
			ps_cursor.close()
			CloseDB(ps_connection)      
			return 'success'
	except Exception as e :
		 return 'error'

	
	