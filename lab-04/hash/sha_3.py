from hashlib import sha3_256

def sha3(input_bytes: bytes) -> bytes:
    hasher = sha3_256()
    hasher.update(input_bytes)
    return hasher.digest()
