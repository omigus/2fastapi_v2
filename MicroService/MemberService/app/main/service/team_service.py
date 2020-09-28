from flask import   jsonify 
import json
import requests
import os
from app.main.database import InitDB , CloseDB
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime, pytz
import uuid
from psycopg2.extras import RealDictCursor
tz = pytz.timezone('Asia/Bangkok')


def findAll_Company_admin(company_id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor(cursor_factory=RealDictCursor)
			query = (" select team.team_id , team.team_public_id , team.team_name , team.team_avatar , team.team_is_active ,(SELECT extract(epoch from team.created_on) as TIME ), team.admin_id , team.company_id "
			  			" from team inner join company on team.company_id = company.company_id "
							 " where company.company_id = %s "
			 )
			ps_cursor.execute(query, (company_id  , ) ) 
			all_team_data = ps_cursor.fetchall()
			ps_cursor.close()
			CloseDB(ps_connection)  
			return ['success' , all_team_data , 200]
	except Exception as e :
		print(e)
		return ['failed','cant not find team' , 200]

def findteamMember_details(team_id):
	try:
		ps_connection = InitDB()
		if (ps_connection):
			ps_cursor = ps_connection.cursor(cursor_factory=RealDictCursor)
			query = (" select users.user_is_active , users.user_id,users.user_public_id , users.user_username , userdetails.userdetails_firstname "
			 					" ,userdetails.userdetails_lastname  ,userdetails.userdetails_lastname  ,userdetails.userdetails_employee_id  ,userdetails.userdetails_phone , userdetails.userdetails_email,userdetails.userdetails_position , userdetails.userdetails_avatar "
								 " from team_has_users "
			 					" inner join users on users.user_id = team_has_users.user_id  "
								 " left join userdetails on userdetails.user_id = users.user_id "
								 " where team_id = %s "
							)
			ps_cursor.execute(query ,( team_id , ))
			team_member = ps_cursor.fetchall()
			ps_cursor.close()
			CloseDB(ps_connection)  
			return ['success' , team_member , 200]
	except Exception as e:
		print (e)
		return ['failed','cant not find team' , 200]

def findTeam_ById(id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor(cursor_factory=RealDictCursor)
			query = (
								" select * from team "
								" where team.team_id = %s "
			 				)
			ps_cursor.execute(query, (id , ) ) 
			team = ps_cursor.fetchone()
			team["created_on"] = team["created_on"].timestamp()
			if team is None:
				team = []
			ps_cursor.close()
			CloseDB(ps_connection)      
			return ['success' , team , 200]
	except Exception as e :
		print(e)
		return ['failed','cant not find team' , 200]


def InsertTeam(team_name , team_avatar , admin_id , company_id):
	dt = datetime.datetime.now(tz)
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
		print(e)
		return 'error'


def EditTeam(team_name , company_id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("  UPDATE  team SET  team_name = %s WHERE company_id = %s " )
			ps_cursor.execute(query, (team_name ,company_id , ) ) 
			ps_connection.commit()
			ps_cursor.close()
			CloseDB(ps_connection)      
			return 'success'
	except Exception as e :
		 return 'error'

def findteamMember(team_id):
	try:
		ps_connection = InitDB()
		if (ps_connection):
			ps_cursor = ps_connection.cursor()
			query = (" select user_id from team_has_users where team_id = %s ")
			ps_cursor.execute(query ,( team_id , ))
			team_member = ps_cursor.fetchall()
			ps_cursor.close()
			CloseDB(ps_connection)  
			return team_member
	except Exception as e:
		return 'error'
			

def InsertTeamMember(team_id , user_id):
	exists_user = False
	all_member = findteamMember(team_id)
	if all_member == 'error' :
		return ['failed','error could not find member in team' , 200]
	for member in all_member:
		if int(member[0]) == int(user_id) :
			exists_user = True
	if exists_user == True :
		return ['failed','error member already in team member' , 200]
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
		return ['failed','user not in user table' , 200]

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
def RemoveTeam(team_id ) :
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = ("  delete from team where team_id = %s  " )
			ps_cursor.execute(query, (team_id , ) ) 
			ps_connection.commit()
			ps_cursor.close()
			CloseDB(ps_connection)      
			return 'success'
	except Exception as e :
		print(e)
		return 'error'

	
	