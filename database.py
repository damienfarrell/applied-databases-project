from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import pymysql
import sys
from pymysql.cursors import DictCursor

load_dotenv()
# Neo4j connection settings
DATABASE_NEO4J_URI = os.getenv('DATABASE_NEO4J_URI')
DATABASE_NEO4J_USER = os.getenv('DATABASE_NEO4J_USER')
DATABASE_NEO4J_PASSWORD = os.getenv('DATABASE_NEO4J_PASSWORD')
DATABASE_NEO4J_AUTH = (DATABASE_NEO4J_USER, DATABASE_NEO4J_PASSWORD)

# MySQL connection settings
DATABASE_MYSQL_HOST = os.getenv('DATABASE_MYSQL_HOST')
DATABASE_MYSQL_USER = os.getenv('DATABASE_MYSQL_USER')
DATABASE_MYSQL_PASSWORD = os.getenv('DATABASE_MYSQL_PASSWORD')
DATABASE_MYSQL_DB = os.getenv('DATABASE_MYSQL_DB')

def connect_mysql():
    try:
        conn = pymysql.connect(
            host=DATABASE_MYSQL_HOST,
            user=DATABASE_MYSQL_USER,
            password=DATABASE_MYSQL_PASSWORD,
            database=DATABASE_MYSQL_DB,
            cursorclass=DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            # print(f"Connected to MySQL Server version {version['VERSION()']}")
        return conn
    except pymysql.MySQLError as e:
        print(f"Connection failed: {e}")
        return None

def connect_neo4j():
    try:
        driver = GraphDatabase.driver(DATABASE_NEO4J_URI, auth=DATABASE_NEO4J_AUTH)
        return driver
    except Exception as e:
        print(f"Failed to create a driver: {e}")
        return None