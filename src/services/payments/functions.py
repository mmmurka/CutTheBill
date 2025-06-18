import random
import string

def generate_payment_code(length=6) -> str:
    return '#' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
