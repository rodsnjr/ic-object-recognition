from uuid import uuid4


def generate_uid() -> str:
    return str(uuid4())
