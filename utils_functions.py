from cryptography.fernet import Fernet
import os



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




# Stores password as an encrypted string, which makes a prettier output for password retrieval
# Takes a string --> password
# Encrypt it
# Convert it from bytes --> string
# Return the encrypted sting
def encrypt_pw(password):
    encrypted_pw = fernet.encrypt(password.encode('utf-8'))
    encrypted_str = encrypted_pw.decode('utf-8')
    return encrypted_str


# Method for decrypting password
# Takes encrypted string from db
# Converts it back to bytes
# Decrypts it with fernet key
# Return original plain text password
def decrypt_pw(encrypted_pw):
    encrypted_pw = encrypted_pw.encode('utf-8')
    password = fernet.decrypt(encrypted_pw).decode('utf-8')
    return password