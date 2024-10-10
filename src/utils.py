import re

def validate_username(username):
    return re.match("^[a-zA-Z0-9_]+$", username) is not None

def validate_password(password):
    # Example: at least 8 characters, contains a number and a letter
    return len(password) >= 8 and re.search("[a-zA-Z]", password) and re.search("[0-9]", password)
