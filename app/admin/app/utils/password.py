import hashlib

def password_hash(password):
    m = hashlib.md5()
    m.update(bytes(password))
    return m.hexdigest()