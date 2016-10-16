import base64
import bcrypt
import hashlib

def _sha256_base64(password):
    return base64.b64encode(hashlib.sha256(
        password.encode('utf-8')).digest())

def hash(password):
    return bcrypt.hashpw(
        _sha256_base64(password),
        bcrypt.gensalt(12))

def verify(password, pwhash):
    return bcrypt.checkpw(
        _sha256_base64(password),
        pwhash)
