import hashlib


def normalize_username(value):
    clean = value.strip().lower()
    return remove_spaces(clean)


def remove_spaces(value):
    return value.replace(" ", "")


def hash_token(value):
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return shorten_hash(digest)


def shorten_hash(value):
    return value[:16]
