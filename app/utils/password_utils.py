import bcrypt

def hash_password(password_input):
    return bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(password_input, hashed_password):
    return bcrypt.checkpw(password_input.encode('utf-8'), hashed_password.encode())
