import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()


threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(1, 100,user = os.getenv('DB_USER'),
											  password =os.getenv('DB_PASSWORD'),
											  host = os.getenv('HOST'),
											  port = os.getenv('PORT'),
											  database = os.getenv('DATABASE'))

def InitDB():
	return threaded_postgreSQL_pool.getconn()
        
def CloseDB(ps_connection):
	ps_cursor = ps_connection.cursor()
	ps_cursor.close()
	threaded_postgreSQL_pool.putconn(ps_connection)