from hashlib import blake2b

def blake2(input_bytes: bytes) -> bytes:
    hasher = blake2b()
    hasher.update(input_bytes)
    return hasher.digest()
