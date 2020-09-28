import flask
import requests
import os
from app.main.database import InitDB , CloseDB

def findByPublic_company(company_public_id):
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
def findIdByPublic_company(company_public_id):
	try:
		ps_connection  = InitDB()
		if(ps_connection):
			uuid_entry = str(company_public_id) 
			ps_cursor = ps_connection.cursor()
			query = ("select company_id from company where company_public_id = %s ")
			ps_cursor.execute(query, (uuid_entry , ) )
			company = ps_cursor.fetchone()
			ps_cursor.close()   
			CloseDB(ps_connection)     
			return company
	except(Exception ) as e:
		return 'error'


