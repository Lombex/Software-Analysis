def validate_input(input_type, value):
    if input_type == 'username':
        return validate_username(value)
    elif input_type == 'password':
        return validate_password(value)
    elif input_type == 'email':
        return validate_email(value)
    elif input_type == 'age':
        return validate_age(value)
    elif input_type == 'weight':
        return validate_weight(value)
    elif input_type == 'phone':
        return validate_phone(value)
    elif input_type == 'name':
        return validate_name(value)
    elif input_type == 'zip_code':
        return validate_zip_code(value)
    else:
        return False

def validate_username(username):
    # Allow usernames between 8 and 20 characters
    if len(username) < 8 or len(username) > 20:
        return False
    
    # The first character must be alphabetic or an underscore
    if not (username[0].isalpha() or username[0] == '_'):
        return False
    
    # Valid characters are alphabets, digits, underscores, dots, and single quotes
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.'")
    
    # Ensure every character is valid
    for char in username:
        if char not in allowed_chars:
            return False
    
    return True

def validate_password(password):
    if len(password) < 12 or len(password) > 30:
        return False

    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    # Special characters allowed in password
    special_chars = "~!@#$%&_-+=`|\(){}[]:;'<>,.?/"

    for char in password:
        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        elif char in special_chars:
            has_special = True

    # Check if password contains all required character types
    return has_lower and has_upper and has_digit and has_special

def validate_email(email):
    # Simplified email validation without regex
    if "@" not in email or "." not in email:
        return False
    local, domain = email.split('@', 1)
    if len(local) < 1 or len(domain) < 3 or '.' not in domain:
        return False
    return True

def validate_age(age):
    try:
        age = int(age)
        return 0 < age < 150
    except ValueError:
        return False

def validate_weight(weight):
    try:
        weight = float(weight)
        return 0 < weight < 1000
    except ValueError:
        return False

def validate_phone(phone):
    # Dutch phone number format: +31-6-DDDDDDDD
    if not phone.startswith("+31-6-"):
        return False
    phone_number = phone[6:]  # Extract number after +31-6-
    
    # Ensure there are exactly 8 digits after +31-6-
    return len(phone_number) == 8 and phone_number.isdigit()

def validate_name(name):
    # Ensure name is at least 2 characters and contains only alphabetic characters
    return len(name) >= 2 and name.isalpha()

def validate_zip_code(zip_code):
    # Dutch zip code format: 4 digits followed by 2 letters
    if len(zip_code) != 6:
        return False
    
    digits_part = zip_code[:4]
    letters_part = zip_code[4:]
    
    # Check if first part is digits and second part is letters
    return digits_part.isdigit() and letters_part.isalpha() and letters_part.isupper()

def validate_city(city, valid_cities):
    return city in valid_cities

def detect_suspicious_input(input_string):
    suspicious_patterns = [
        "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "UNION", "FROM", "WHERE",
        "--", "/*", "*/", "@@", "@", "CHAR(", "DECLARE", "CAST(", "CONVERT(",
        "EXEC(", ";", "'+", "\"", "OR 1=1", "OR '1'='1", "INFORMATION_SCHEMA",
        "LOAD_FILE", "INTO OUTFILE"
    ]
    # Check for suspicious patterns in a case-insensitive manner
    input_lower = input_string.lower()
    for pattern in suspicious_patterns:
        if pattern.lower() in input_lower:
            return True
    return False
