import re

def validate_username(username):
    """
    Validate username based on specified criteria:
    - Starts with a letter or underscore
    - 8 to 10 characters long
    - Allows letters, numbers, underscores, periods, apostrophes
    """
    return bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_.']{7,9}$", username))

def validate_password(password):
    """
    Validate password based on specified criteria:
    - At least 12 characters long
    - Contains at least one lowercase letter
    - Contains at least one uppercase letter
    - Contains at least one digit
    - Contains at least one special character from ~!@#$%&_\-+=`|()\{}[]:;'<>,.?/
    """
    return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|()\{}[\]:;'<>,.?/]).{12,30}$", password))

def validate_email(email):
    """
    Validate email address based on basic format
    """
    return bool(re.match(r"^[^@]+@[^@]+\.[^@]+$", email))

def validate_age(age):
    """
    Validate age as a positive integer
    """
    try:
        age = int(age)
        return age > 0
    except ValueError:
        return False

def validate_weight(weight):
    """
    Validate weight as a positive float
    """
    try:
        weight = float(weight)
        return weight > 0
    except ValueError:
        return False

def validate_phone(phone):
    """
    Validate phone number as a 10-digit string
    """
    return bool(re.match(r"^\d{10}$", phone))
