import random
import string


def domain_random(amount):
    '''
    Randomize a number of domains.
    :param amount: The number of domains to generate
    :return: A list of randomly generated domains.
    '''
    return [''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(random.randint(1,63))) + random.choice(['.com', '.org']) for _ in range(amount)]


def client_id_random():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(12))

if __name__ == '__main__':
    print(client_id_random())