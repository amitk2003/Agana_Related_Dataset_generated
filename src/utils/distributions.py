import random

def weighted_choice(choices):
    """
    choices = [(value, weight), ...]
    """
    total = sum(weight for _, weight in choices)
    r = random.uniform(0, total)
    upto = 0
    for value, weight in choices:
        if upto + weight >= r:
            return value
        upto += weight
