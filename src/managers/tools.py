# src/managers/tools.py
import secrets
import string

def generate_password(length=16):
    """This function generates a unique password using secrets."""
    possible_characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    password = ''.join(secrets.choice(possible_characters) for _ in range(length))
    return password
