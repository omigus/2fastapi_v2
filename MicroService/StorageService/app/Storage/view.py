from flask import Flask, request, jsonify, make_response, Blueprint
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import CombinedMultiDict
import jwt
import json
from functools import wraps
from app import SECRET_KEY, EndPoint , UPLOADED_FOLDER , ALLOWED_EXTENSIONS 
import urllib
import os
import requests
import collections
from app.Storage.helper.helperFunc import token_required , root_dir  , getFolderSize
from app.Storage.database import CloseDB , InitDB

StorageService = Blueprint("StorageService", __name__, url_prefix=EndPoint + "/v2")


@StorageService.route("/create_storage/<company_public_id>", methods=["POST"])
@token_required
def Create_Folder_Company(current_user, company_public_id):
    if not company_public_id:
        return jsonify({"status": "failed", "message": "missing company_public_id" }), 404
    try:
        if not os.path.exists(UPLOADED_FOLDER+company_public_id):
            os.mkdir(UPLOADED_FOLDER+company_public_id)
            return jsonify({"status": "success", "message": "folder created"}), 201
        else:
            return jsonify({"status": "success", "message": "folder already created"}), 200
    except Exception as e :
        print(e)
        return jsonify({"status": "failed", "message": "cant create folder company" + str(e)}), 500


@StorageService.route("/storage/<company_public_id>", methods=["GET"])
@token_required
def Company_current_storage_size(current_user, company_public_id):
    if not company_public_id:
        return jsonify({"status": "failed", "message": "missing company_public_id" }), 404
    try:
        ps_connection  = InitDB()
        if(ps_connection):
            ps_cursor = ps_connection.cursor()
            query = (   " select system_create_limit_storage from system_create_limit  "
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
            limit_storage = ps_cursor.fetchone()
            if limit_storage is None :
                limit_storage = 0
            else :
                limit_storage = limit_storage[0]
            ps_cursor.close()
            CloseDB(ps_connection)
           
    except Exception as e:
        return jsonify({"status": "failed", "message": "could not find company_public_id" }), 500
    if not os.path.exists(UPLOADED_FOLDER+company_public_id):
        return jsonify({"status": "failed", "message": "could not find folder by company_public_id"}), 404
    try:
        if  os.path.exists(UPLOADED_FOLDER+company_public_id):
            current_folder_size = getFolderSize(UPLOADED_FOLDER+company_public_id)
        
            return jsonify({"status": "success", "current_folder_size":  current_folder_size , "limit_folder_size" : limit_storage}), 200
    except Exception as e :
        return jsonify({"status": "failed", "message": "could not calculate folder size" + str(e)}), 500

