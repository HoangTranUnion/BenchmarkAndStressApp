import re


def validate_domain(domain):
    regex = "\b((xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}\b"
    p = re.compile(regex)
    if len(domain) == 0:
        return False
    if re.search(p, domain):
        return True
    else:
        return False
