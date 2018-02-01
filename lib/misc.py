import random, string


def random_string(N):
    """
    Random string generator
    :param N:
        length
    :return:
        random string
    """
    random_string = ''.join(random.choice(string.ascii_uppercase + string.digits)
            for _ in range(N))
    return random_string