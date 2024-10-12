import datetime

def validate_username(username):
    """
    Validate username based on specified criteria:
    - Starts with a letter or underscore
    - 8 to 10 characters long
    - Allows letters, numbers, underscores, periods, apostrophes ( ' . _ 0 a )
    """
    if not (8 <= len(username) <= 20):                                          #change back!
        return False, "Username should be between 8 and 10 characters long."
    
    if not (username[0].isalpha() or username[0] == '_'):
        return False, "Username should start with a letter or underscore."
    
    allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.'")
    for char in username:
        if char not in allowed_characters:
            return False, "Username can only contain letters, numbers, underscores, periods, and apostrophes."
    
    return True, ""

def validate_name(name):
    """
    Validate name based on specified criteria:
    - At least 2 characters long
    - Only alphabetic characters
    """
    if len(name) >= 2 and name.isalpha():
        return True, ""
    return False, "Name must be at least 2 letters and contain only alphabetic characters."

def validate_password(password):
    """
    Validate password based on specified criteria:
    - At least 12 characters long
    - Contains at least one lowercase letter
    - Contains at least one uppercase letter
    - Contains at least one digit
    - Contains at least one special character from ~!@#$%&_-+=`|(){}[]:;'<>,.?/
    """
    if len(password) < 8:                                                           #change back!
        return False, "Password must be at least 12 characters long."
    
    has_lower = any(char.islower() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in "~!@#$%&_-+=`|(){}[]:;'<>,.?/" for char in password)

    if not has_lower:
        return False, "Password must contain at least one lowercase letter."
    if not has_upper:
        return False, "Password must contain at least one uppercase letter."
    if not has_digit:
        return False, "Password must contain at least one digit."
    if not has_special:
        return False, "Password must contain at least one special character from ~!@#$%&_-+=`|(){}[]:;'<>,.?/"
    
    return True, ""

def validate_email(email):
    """
    Validate email address based on a basic format:
    - Contains exactly one '@' symbol
    - Has a domain part after '@' with at least one dot ('.')
    - There must be characters before '@', and the domain name and extension should not be empty
    """
    if email.count('@') != 1:
        return False, "Email must contain exactly one '@' symbol."
    
    local_part, domain_part = email.split('@')

    if not local_part:
        return False, "Email local part (before '@') cannot be empty."
    
    if '.' not in domain_part:
        return False, "Email domain part must contain at least one '.' symbol."
    
    domain_name, *domain_extension = domain_part.split('.')
    if not domain_name or not all(domain_extension):
        return False, "Domain name and extension cannot be empty."

    return True, ""

def validate_age(age):
    """
    Validate age as a positive integer
    """
    try:
        age = int(age)
        if age > 0:
            return True, ""
        return False, "Age must be a positive integer."
    except ValueError:
        return False, "Age must be a positive integer."

def validate_weight(weight):
    """
    Validate weight as a positive float
    """
    try:
        weight = float(weight)
        if weight > 0:
            return True, ""
        return False, "Weight must be a positive number."
    except ValueError:
        return False, "Weight must be a positive number."

def validate_phone(phone):
    """
    Validate phone number as an 8-digit string
    """
    phone_str = str(phone)
    if len(phone_str) == 8 and phone_str.isdigit():
        return True, ""
    return False, "Phone number must be an 8-digit number."

def validate_membership_id(membership_id):
    """
    Validate membership ID based on specified criteria:
    - Must be 10 characters long
    - First two characters represent the year and cannot exceed the current year
    - Checksum validation
    """
    if len(membership_id) != 10:
        return False, "Invalid length."
    
    id_digits = [int(digit) for digit in membership_id]
    year = int(membership_id[:2])
    current_year = datetime.datetime.now().year % 100

    if year > current_year:
        return False, f"Invalid year {year}, we are still in {current_year}."
    
    checksum = id_digits[-1]
    calculated_checksum = sum(id_digits[:-1]) % 10

    if checksum != calculated_checksum:
        return False, f"Checksum mismatch. Expected {calculated_checksum} but found {checksum}."
    
    return True, "Valid ID."
