import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()


threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 50,user = os.getenv('DB_USER'),
											  password =os.getenv('DB_PASSWORD'),
											  host = os.getenv('HOST'),
											  port = os.getenv('PORT'),
											  database = os.getenv('DATABASE'))
if(threaded_postgreSQL_pool):
        print("Connection pool created successfully using ThreadedConnectionPool")
        
