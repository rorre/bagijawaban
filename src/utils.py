import random
import string


def random_str(size=6, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))
