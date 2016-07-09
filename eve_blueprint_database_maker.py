#!/usr/lib/python3.4

#http://www.blog.pythonlibrary.org/2012/07/18/python-a-simple-step-by-step-sqlite-tutorial/

import sqlite3


conn = sqlite3.connect('DARPA_blueprints.db')

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS 
        All_blueprints (ID INT PRIMAY KEY, time_efficiency INT, type_id INT,
          type_name TEXT, quantity INT, location_id INT, material_efficiency INT,
          run INT)""")

conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS
               Build_Materials (ID INT, price REAL)""")
conn.commit()
