from flask import Blueprint , jsonify 
import json
from app.main.database import threaded_postgreSQL_pool
PurchasedService = Blueprint("PurchasedService", __name__,url_prefix= "/api/v1/")

@PurchasedService.route("/", methods=["GET"])
def test():
    try:
        ps_connection  = threaded_postgreSQL_pool.getconn()
        if(ps_connection):
            print("successfully recived connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            ps_cursor.execute("select * from django_content_type")
            mobile_records = ps_cursor.fetchmany(50)
            print ("Displaying rows from mobile table")
            ps_cursor.close()
            threaded_postgreSQL_pool.putconn(ps_connection)
            return jsonify(mobile_records),200
    except (Exception) as error :
        return jsonify('error' , error),500

