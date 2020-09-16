import flask
import requests
import os
from app.main.database import InitDB , CloseDB


def create_storage(current_user_jwt_token,company_uuid):
	domain_name = os.getenv('DOMAIN_NAME')
	storage_service_url = domain_name + ':5005/api/v2/create_storage/' + company_uuid
	headers = {'Authorization': 'Bearer '+str(current_user_jwt_token)}
	r = requests.post(storage_service_url, headers=headers)
	return r.status_code 

def findByPublic(company_public_id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			uuid_entry = str(company_public_id) 
			ps_cursor = ps_connection.cursor()
			query = ("select * from company where company_public_id = %s ")
			ps_cursor.execute(query, (uuid_entry , ) )
			company = ps_cursor.fetchone()
			ps_cursor.close()   
			CloseDB(ps_connection)     
			return company
	except(Exception ) as e:
		return 'error'

def check_exists_company_users_current(company_public_id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			company_id = findByPublic(company_public_id)
			ps_cursor = ps_connection.cursor()
			query = ("select count(*) from company_users_current where company_id = %s ")
			ps_cursor.execute(query, ( company_id[0] , ) )
			company = ps_cursor.fetchone()
			ps_cursor.close()   
			CloseDB(ps_connection)     
			return company
	except(Exception ) as e:
		print(e)
		return 'error'

def checkcompany_admin_limit(company_public_id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			ps_cursor = ps_connection.cursor()
			query = (   " select  system_create_limit.system_create_limit_admin from system_create_limit  "
						" inner join system_group_limit "
						" on   system_create_limit.system_create_limit_id  = system_group_limit.system_create_limit_id "
						" inner join system_group_all "
						" on "
						" system_group_all.system_group_all_id = system_group_limit.system_group_all_id "
						" inner join company_has_system_group_all "
						" on "
						" company_has_system_group_all.system_group_all_id = system_group_all.system_group_all_id "
						" inner join company "
						" on "
						" company.company_id = company_has_system_group_all.company_id "  
						" where company.company_public_id = %s ")
			ps_cursor.execute(query, (company_public_id,))
			limit_all = ps_cursor.fetchone()
			ps_cursor.close()
			CloseDB(ps_connection)
			return limit_all[0]
	except Exception as e :
		print(e)
		pass
