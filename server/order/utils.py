import uuid

# Generic a random number


def generate_random():
    return str(uuid.uuid4())[:8]


print(generate_random())
