This is a command-line Password Vault application written in Python.
It allows a user to store, retrieve, update, and delete passwords for different services

Requirements
1) mysql-connector-python
2) cryptography
3) bcrypt

pip install -r requirements.txt

*You also need a running MySQL server*

The application uses:
1) MySQL for storing vault entries
2) Fernet encryption from the cryptography library to encrypt passwords
3) bcrypt hashing+salting to protect the master password

Passwords stored in the database are encrypted, and access to the vault it protected with a master password

project-folder/
│
├── database.py
├── main.py
├── utils_functions.py
├── secret.key
├── master_pw.key
└── README.md

main.py
Main application file that runs the password vault
Functions include:
1) Creating or verifying the master password
2) Displaying the vault menu
3) Adding new entries
4) Updating passwords
5) Deleting entries
6) Revealing stored passwords

It connects to the MySQL database and interacts with stored vault entries

database.py
This file is responsible for database setup
It performs two main tasks:
1) Create the database --> password_vault
2) Create the required database table --> vault_entries
3) Running this script initializes the database if it does not already exists

utils_functions.py
This file contains helper functions used for encryption and decryption
Functions:
encrypt_pw(password)
1) Encrypts a password using Fernet encryption
2) Converts it to a string before storing it in the database
decrypt_pw(encrypted_pw)
1) Converts encrypted string back to bytes
2) Decrypts it using the Fernet key
3) Returns the original plaintext password

Security Features:
Master Password Protection
1) The vault requires a master password to access
2) It is hashed using bcrypt and stored in master_pw.key (not recommended)

Encryption
1) All stored passwords are encrypted using Fernet symmetric encryption
2) the encryption key is stored in secret.key (not recommended)

Limited Login attempts
1) The user has 3 attempts to enter the correct master password
2) after 3 failed attempts, the program exits

Database configuration
The program currently connects using:
host = 127.0.0.1
user = user_of_choice(root) --> Recommended to create a different user with as little privileges as necessary to perform the operations
password = your password
If your MySQL credentials are different, update them in:
database.py
main.py

How to run:
1) Setup the database --> Run python database.py
2) Start the password vault --> python main.py

First time setup
When running the program for the first time:
1) A secret encryption key is generated
2) You will be asked to create a master password

Vault Menu
After logging in, you can:
A - Add a new entry
C - Change a password
D - Delete an entry
R - Reveal password
Q - Quit the vault

Limitations
1) The encryption key (secret.key) must not be lost --> without it, stored passwords cannot be decrypted
2) Master password and encryption key are stored in files. This is not recommended security practice, and a different method for storage should be researched and implemented.

