import mysql.connector

def create_database():
    db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password=''
)

    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS password_vault")

    db.commit()
    cursor.close()

#############################################################################

def create_tables():

    db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='password_vault'
)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS vault_entries(
                   id INT PRIMARY KEY AUTO_INCREMENT, 
                   username VARCHAR(100), 
                   service VARCHAR(100), 
                   password TEXT NOT NULL
                   )
                   """)
    db.commit()
    cursor.close()
    print('\n')
    print('***Database configuered and ready***')
    print('\n')

create_database()
create_tables()


