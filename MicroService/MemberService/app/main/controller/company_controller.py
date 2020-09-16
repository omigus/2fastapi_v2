from flask import Blueprint , jsonify ,request
import json
import uuid 
import datetime
import psycopg2
from app.main.database import InitDB , CloseDB
from app.main.helper.token import token_required
import os
import requests
from app.main.service.company_service import create_storage

CompanyService = Blueprint("CompanyService", __name__,url_prefix= "/api/v2")
@CompanyService.route("/company", methods=["POST"])
@token_required
def RegisterCompany_with_groupsystem(current_user):
    if request.content_type != 'application/json':
        return jsonify({"status": "failed", "message": "Invalid content-type. Must be application/json." }), 400
    try:
        params = request.get_json()
        company_name = params["company_name"]
        uuid_entry = str(uuid.uuid4()) 
        ps_connection  = InitDB()
        if(ps_connection):
            ps_cursor = ps_connection.cursor()
            query = ("  insert into company( company_name , company_public_id , company_is_active ,created_on ) values ( %s , %s , %s ,%s )" )
            ps_cursor.execute(query, (company_name, uuid_entry , '1', datetime.datetime.now() ) )
            ps_connection.commit()
            ps_cursor.close()
            CloseDB(ps_connection)      
            token = request.headers["Authorization"]
            access_token = token.split(" ")[1]
            status_code  = create_storage(access_token ,uuid_entry )    
            if int (status_code) == 201 :   
                return jsonify({"status" : 'success' , "company_public_id" : uuid_entry } ),201
    except (Exception, psycopg2.Error) as error:
        return jsonify({'status' : 'falied' , "message" :  error} ),500

