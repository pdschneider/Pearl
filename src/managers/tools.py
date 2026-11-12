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


PASSWORD_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "generate_password",
        "description": "Generates a random secure password.",
        "parameters": {
            "type": "object",
            "properties": {
                "length": {"type": "integer", "description": "Length of the password in characters."}
            },
            "required": []
        }
    }
}
