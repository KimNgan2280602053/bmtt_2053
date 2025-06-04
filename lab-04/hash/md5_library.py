import hashlib

def calculate_md5(input_text: str) -> str:
    return hashlib.md5(input_text.encode('utf-8')).hexdigest()
