import secrets


def generate_payment_code() -> str:
    return secrets.token_hex(16)
