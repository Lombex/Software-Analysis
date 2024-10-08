def validate_username(username):
    """
    Validate username based on specified criteria:
    - Starts with a letter or underscore
    - 8 to 10 characters long
    - Allows letters, numbers, underscores, periods, apostrophes ( ' . _ 0 a )
    """
    if not (8 <= len(username) <= 10):
        print("Username should be between 8 and 10 characters long.")
        return False
    
    if not (username[0].isalpha() or username[0] == '_'):
        print("Username should start with a letter or underscore.")
        return False
    
    allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.'")
    for char in username:
        if char not in allowed_characters:
            print("Username can only contain letters, numbers, underscores, periods, and apostrophes.")
            return False
    
    return True

def validate_name(name):
    if len(name) >= 2 and name.isalpha():
        return True
    return False

def validate_password(password):
    """
    Validate password based on specified criteria:
    - At least 12 characters long
    - Contains at least one lowercase letter
    - Contains at least one uppercase letter
    - Contains at least one digit
    - Contains at least one special character from ~!@#$%&_-+=`|(){}[]:;'<>,.?/
    """
    if len(password) < 12:
        return "Password must be at least 12 characters long."
    
    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False
    
    special_characters = set("~!@#$%&_-+=`|(){}[]:;'<>,.?/")

    for char in password:
        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    if not has_lower:
        print("Password must contain at least one lowercase letter.")
        return False
    if not has_upper:
        print("Password must contain at least one uppercase letter.")
        return False
    if not has_digit:
        print("Password must contain at least one digit.")
        return False
    if not has_special:
        print("Password must contain at least one special character from ~!@#$%&_-+=`|(){}[]:;'<>,.?/")
        return False
    
    return True

def validate_email(email):
    """
    Validate email address based on a basic format:
    - Contains exactly one '@' symbol
    - Has a domain part after '@' with at least one dot ('.')
    - There must be characters before '@', and the domain name and extension should not be empty
    """
    if email.count('@') != 1:
        print("Email must contain exactly one '@' symbol.")
        return False
    local_part, domain_part = email.split('@')

    if not local_part:
        print("Email local part (before '@') cannot be empty.")
        return False
    
    if '.' not in domain_part:
        print("Email domain part must contain at least one '.' symbol.")
        return False
    
    domain_name, *domain_extension = domain_part.split('.')
    if not domain_name or not all(domain_extension):
        print("Domain name and extension cannot be empty.")
        return False

    return True

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
    if len(str(phone)) != 10:
        return False
    return True
