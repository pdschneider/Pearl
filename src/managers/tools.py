# src/managers/tools.py
import logging
import secrets
import string


def generate_password(length=16):
    """This function generates a unique password using secrets."""
    try:
        possible_characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        password = ''.join(secrets.choice(possible_characters) for _ in range(int(length)))
    except Exception as e:
        logging.error(f"Unable to generate password due to: {e}")
        password = f"Error: {e}"
    return password
