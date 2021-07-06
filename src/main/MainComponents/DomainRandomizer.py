import random
import string


def domain_random(amount):
    return [''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(random.randint(1,63))) + random.choice(['.com', '.org']) for _ in range(amount)]


if __name__ == '__main__':
    print(domain_random(12))