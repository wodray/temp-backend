from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


def get_password_hash(password):
    return ph.hash(password)


def verify_password(plain_password, hashed_password):
    if ph.check_needs_rehash(hashed_password):
        print("needs_rehash")
    try:
        ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    else:
        return True
