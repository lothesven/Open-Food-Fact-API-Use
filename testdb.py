# -*- coding: utf-8 -*

from __future__ import print_function
import config as cf

from datetime import date, datetime, timedelta

import mysql.connector
from mysql.connector import errorcode

history_values = {
            "user_ID": 1, 
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
            "action": "this is an action", 
            "result": "this is a result"
            }

cnx = mysql.connector.connect(**cf.CREDENTIALS) # connexion handling instance
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(cf.DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(cf.DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(cf.DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(cf.DB_NAME))
        cnx.database = cf.DB_NAME
    else:
        print(err)
        exit(1)

for table_name in cf.TABLES:
    table_description = cf.TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.execute(cf.HISTORY_INSERT, history_values)
cnx.commit()

cursor.close()
cnx.close()
