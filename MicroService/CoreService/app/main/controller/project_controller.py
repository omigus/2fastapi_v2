from flask import Blueprint , jsonify ,request
import json
import uuid 
import datetime
import psycopg2
from app.main.database import InitDB , CloseDB
from app.main.helper.token import token_required , token_required_admin
from app.main.helper.http_response import http_response
import os
import requests


ProjectService = Blueprint("ProjectService", __name__,url_prefix= "/api/v2")
@ProjectService.route("/project", methods=["POST"])
@token_required_admin
def start_project(current_user):
    if request.content_type != 'application/json':
        data = ['failed' , 'Invalid content-type. Must be application/json.' , 400]
        return http_response(data)
    

