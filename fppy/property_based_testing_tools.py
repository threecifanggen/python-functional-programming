from itertools import chain
from random import randint, choices
from string import ascii_letters, digits, punctuation, whitespace

all_chars = ascii_letters + digits + punctuation + whitespace

def int_generator(
        num=200,
        max_v=65535,
        min_v=-65535,
        must_have=[0]
    ):
    return chain(
        (randint(min_v, max_v) for _ in range(num - len(must_have))),
        must_have
    )
    
def str_generator(
        num=200,
        min_length=0,
        max_length=320,
        must_have=["", digits, punctuation, whitespace],
        choice_chars=all_chars
    ):
    return chain(
        (
            "".join(choices(choice_chars, k=randint(min_length, max_length)))
            for _ in range(num - len(must_have))
        ),
        must_have
    )