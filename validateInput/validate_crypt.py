import re
import string
import bcrypt

# Constants
STATES_IN_INDIA = ['andhra pradesh', 'arunachal pradesh', 'assam', 'bihar', 'chhattisgarh', 'goa', 'gujarat', 'haryana', 'himachal pradesh', 'jharkhand', 'karnataka', 'kerala', 'madhya pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'punjab', 'rajasthan', 'sikkim', 'tamil nadu', 'telangana', 'tripura', 'uttar pradesh', 'uttarakhand', 'west bengal', 'andaman and nicobar islands', 'chandigarh', 'dadra and nagar haveli and daman and diu', 'delhi', 'lakshadweep', 'puducherry', 'ladakh', 'jammu and kashmir']

def validate_single_name(name):
    return name.isalpha() and len(name) <= 20

def validate_name(firstName, lastName):
    for name in [firstName, lastName]:
        if not name or not name.isalpha() or len(name) > 20:
            return False
    return True

def validate_phone_number(phoneNumber):
    return phoneNumber.isdigit() and len(phoneNumber) == 10

def validate_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email)) and len(email) <= 50

def validate_gender(gender):
    return gender.lower() in ['male', 'female', 'other']

def validate_address(address):
    return len(address) <= 50

def validate_state(state):
    return state.lower() in STATES_IN_INDIA

def validate_password(password):
    conditions = [
        any(char.isupper() for char in password),
        any(char.islower() for char in password),
        any(char.isdigit() for char in password),
        any(char in string.punctuation for char in password),
        8 <= len(password) <= 20
    ]
    return all(conditions)

def validate_all(firstName, lastName, phoneNumber, email, gender, address, state, password):
    validators = [
        validate_name(firstName, lastName),
        validate_phone_number(phoneNumber),
        validate_email(email),
        validate_gender(gender),
        validate_address(address),
        validate_state(state),
        validate_password(password)
    ]
    if not all(validators):
        raise Exception("Validation failed")
    return True

def validate_key(key, value):
    if key not in ['firstName', 'lastName', 'phoneNumber', 'email', 'gender', 'address', 'state', 'password']:
        return False
    if key == 'firstName' or key == 'lastName':
        return validate_single_name(value)
    
    if key == 'phoneNumber':
        return validate_phone_number(value)
    
    if key == 'email':
        return validate_email(value)
    
    if key == 'gender':
        return validate_gender(value)
    
    if key == 'address':
        return validate_address(value)
    
    if key == 'state':
        return validate_state(value)
    
    if key == 'password':
        return validate_password(value)
    
    return False



# Cryptography Functions
def cryptPassword(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def checkPassword(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
