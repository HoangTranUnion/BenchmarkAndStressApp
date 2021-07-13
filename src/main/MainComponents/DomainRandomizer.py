import random
import string


def domain_random(amount):
    '''
    Randomize a number of domains.
    :param amount: The number of domains to generate
    :return: A list of randomly generated domains.
    '''
    return [''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(random.randint(1,63))) + random.choice(['.com', '.org']) for _ in range(amount)]
