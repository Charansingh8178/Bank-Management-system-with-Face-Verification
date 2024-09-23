 # TO CREATE TABLE 
import mysql.connector as sql

conn = sql.connect(host='localhost', user='root', passwd='charansingh', database='BANK')
c1 = conn.cursor()

if conn.is_connected():
    print("Connection successful")
else:
    print("Error try later again")

def table_creation():
    create_user_table = """CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), contact INT(12), dob VARCHAR(40),unique_id INT(50),City VARCHAR(40), deposit VARCHAR(255), password VARCHAR(255))"""
    with conn.cursor() as cursor:
        cursor.execute(create_user_table)
        conn.commit()

table_creation()
