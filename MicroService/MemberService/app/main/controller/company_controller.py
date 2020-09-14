from flask import Blueprint , jsonify 
import json
from app.main.database import InitDB , CloseDB
CompanyService = Blueprint("CompanyService", __name__,url_prefix= "/api/v1/")

@CompanyService.route("/", methods=["GET"])
def GetAllCompany():
    try:
        ps_connection  = InitDB()
        if(ps_connection):
            ps_cursor = ps_connection.cursor()
            ps_cursor.execute("select * from django_content_type")
            mobile_records = ps_cursor.fetchmany(50)
            ps_cursor.close()
            CloseDB(ps_connection)
            return jsonify(mobile_records),200
    except (Exception) as error :
        return jsonify('error' , error),500

