import bcrypt
import mysql.connector
import time
import os
from utils_functions import encrypt_pw, decrypt_pw
from cryptography.fernet import Fernet


db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='K3ix89aem',
    database='password_vault'
    )


KEY_FILE = "secret.key"

# Checking if the file exists, If not, a new file is generated
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'wb') as file:
        file.write(Fernet.generate_key())
        

#If the file exist, load it to use it in the application
with open(KEY_FILE, 'rb') as file:
    key = file.read()

# Initialising the Fernet key for to use for the encryption
fernet = Fernet(key)

MASTER_PW = 'master_pw.key'


cursor = db.cursor()




# db.commit()
# cursor.close()



def user_entries():
    
    program_on = True
    while program_on == True:


        
        
        
        user_choice_loop = True
        while user_choice_loop == True:

            cursor = db.cursor()

            sql = "SELECT id, username, service FROM vault_entries"
            cursor.execute(sql)
            entries = cursor.fetchall()
            print('-' * 53)
            print('Vault entries overview:')
            print('-' * 53)
                



                # the for-loop goes throug the elements in the tuple and prints them
            for entry in entries:
                print(f'[{entry[0]}] username: {entry[1]} | service: {entry[2]} | password: ')



            prompt_1 = "Add a new entry, press 'A'"
            prompt_2 = "Change a password, press 'C': "
            prompt_3 = "Delete an entry, press 'D': "
            prompt_4 = "Reveal password for an entry, press 'R': "
            prompt_5 = "Exit the vault, press 'Q': "

            print('-' * 53)

            

            user_choice = input(f'\n{prompt_1}\n{prompt_2}\n{prompt_3}\n{prompt_4}\n{prompt_5}\n\n').lower()
        
            
            if user_choice == 'a':
                print('-'*53)
        
                
                
                username = input('Insert a new username: ')
                service = input('Insert a new service: ')
                password = input('Insert a new password: ')

                # Uses the encrypt_pw function to encrypt and store the password in the database as a string
                encrypted_hash = encrypt_pw(password)

                cursor = db.cursor()

                sql = "INSERT INTO vault_entries(username, service, password) VALUES (%s, %s, %s)"
                val = username, service, encrypted_hash
                cursor.execute(sql, val)
                print('Adding entries')
                db.commit()
                time.sleep(1)
                print('.', end='\r')
                time.sleep(1)
                print('..', end='\r')
                time.sleep(1)
                print('...', end='\r')
                cursor.close()
                print('\nNew entries successfully added!\n')
                

            # Elif statement for changing a password
            elif user_choice == 'c':
                try:
                    user_choice_id = int(input("Select a number from available id's in []: ")) 
                except ValueError:
                    print('\n***Invalid input. Please enter a number***\n')
                    continue
            
                
                user_choice_pw = input('\nPlease provide the new password: ')
                sql = "UPDATE vault_entries SET password = %s WHERE id = %s"

                #Using encrypt_pw function to encode the password
                hashed_pw = encrypt_pw(user_choice_pw)
                val = (hashed_pw, user_choice_id)

                cursor.execute(sql,val)
                db.commit()
                print('\nPassword successfully updated\n')
            
                
                    

            # Elif statement for deleting an entire vault entry
            elif user_choice == 'd':
                try:
                    user_choice_id = int(input("Select a number from available id's in []: ")) 
                except ValueError:
                    print('\n***Invalid input. Please enter a number***')
                    continue
                sql = "DELETE FROM vault_entries WHERE id = %s "
                val = (user_choice_id,)

                cursor.execute(sql,val)
                db.commit()
                print('\nEntry successfully deleted\n')

            # Elif statement for revealing a username/service password
            elif user_choice == 'r':
                try:
                    user_choice_id = int(input("Select a number from available id's in []: ")) 
                except ValueError:
                    print('\n***Invalid input. Please enter a number***\n')
                    continue
                sql = "SELECT password FROM vault_entries WHERE id = %s"
                val = (user_choice_id,)
                cursor.execute(sql, val)
                hashed_pw = cursor.fetchone()
                db.commit()

                # Password is presented as a tuple, needs to be a string to be able to decode it
                passwd_str = ''.join(hashed_pw)
                password = decrypt_pw(passwd_str)
                print(f'\nYour password is: {password}\n')
                

            elif user_choice == 'q':
                print('\n')
                print('***Vault exited***')
                program_on = False
                cursor.close()
                exit()



def set_password():

    print('\n')
    print(f'Secret key generated and stored in {KEY_FILE}')
    print('\n')

    print('Password Vault')

    password = input('Set your Master Password: ')
    print(f'\nMaster password created and stored in {MASTER_PW}')
    if password:
        with open(MASTER_PW, 'wb') as file:
                #Generates a salt for the password, making sure it's unique
                salt = bcrypt.gensalt()
                # Storing the password as an encoded variable
                hashed = password.encode('utf-8')
                # Hashing the password + adding salt
                hashed_pw = bcrypt.hashpw(hashed, salt)
                file.write(hashed_pw)

def password_verify():
    with open(MASTER_PW, 'rb') as file:
        stored_hash = file.read()

        
        user_password = input('Enter master password: ').encode('utf-8')

        if bcrypt.checkpw(user_password, stored_hash):
            print('\nWelcome to your password vault!\n')
            return True
        
        else:
            return False
            
            
        
            

def master_pw_exists():
    if not os.path.exists(MASTER_PW):
        # Password does not exist
        return False
    else:
        return True





if not master_pw_exists():
    set_password()
    user_entries()
        

count = 0
while count < 3:
    if password_verify():
        user_entries()
        break
    else:
        print('Wrong password. Try again.')
        count += 1

if count == 3:
    print('Too many failed attempts. Vault exited')
    exit()

