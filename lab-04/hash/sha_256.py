import hashlib

def calculate_sha256_hash(input_text: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(input_text.encode('utf-8'))
    return sha256.hexdigest()
