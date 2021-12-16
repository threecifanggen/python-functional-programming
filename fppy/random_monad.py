"""无副作用的随机数生成器
"""
from __future__ import annotations
from typing import Dict, Tuple
from dataclasses import dataclass
import string

# from .gt import GenericTypeVar, S

LEN_OF_ASCII_CHAR = len(string.printable)


class RandomMonad:
    """随机数基本类
    """


@dataclass
class RandomInt(RandomMonad):
    """随机Int生成器
    """
    seed: int

    def next_val(self) -> Tuple[RandomInt, int]:
        """生成下一个生成器和随机数
        """
        next_seed =  (self.seed * 0x5DEECE66D + 0xB) &\
                        ((1 << 48) - 1)
        return (RandomInt(next_seed), int(next_seed >> 16))

@dataclass
class RandomStringASCII(RandomMonad):
    """ASCII字符随机生成器
    """
    seed: int

    def next_val(self) -> Tuple[RandomStringASCII, str]:
        """生成下一个生成器和随机字符
        """
        next_seed =  (self.seed * 0x5DEECE66D + 0xB) &\
                        ((1 << 48) - 1)
        val = int(next_seed >> 16) % LEN_OF_ASCII_CHAR
        return (RandomStringASCII(next_seed), string.printable[val])


@dataclass
class RandomFloat(RandomMonad):
    """
    获取0~1内的随机浮点数
    """
    seed: int

    def next_val(self) -> Tuple[RandomFloat, float]:
        """生成下一个生成器和随机浮点数
        """
        next_seed = (self.seed * 0x5DEECE66D + 0xB) &\
                        ((1 << 48) - 1)
        val = (int(next_seed >> 16)) / 4294967296
        return (RandomFloat(next_seed), val)

def random_int_generator(seed: int = 1234):
    """随机int生成器
    """
    while True:
        next_seed, res =  RandomInt(seed).next_val()
        yield res
        yield from random_int_generator(next_seed.seed)

def random_ascii_generator(seed: int = 1234):
    """随机ascii字符生成器
    """
    while True:
        next_seed, res = RandomStringASCII(seed).next_val()
        yield res
        yield from random_ascii_generator(next_seed.seed)

def random_float_generator(seed: int = 1234):
    """随机float生成器
    """
    while True:
        next_seed, res = RandomFloat(seed).next_val()
        yield res
        yield from random_float_generator(next_seed.seed)


VAL_TYPE_DICT: Dict[str, RandomMonad] = {
    "int": RandomInt,
    "ascii": RandomStringASCII,
    "float": RandomFloat
}

def random_val(seed: int = 1234, val_type: str = 'int'):
    """通用随机值生成器
    """
    while True:
        next_seed, res = VAL_TYPE_DICT[val_type](seed).next_val()
        yield res
        yield from random_val(next_seed.seed, val_type)

random_ascii_generator_2 = lambda seed=1234: map(
    lambda x: string.printable[x % LEN_OF_ASCII_CHAR],
    random_int_generator(seed)
)

random_float_generator_2 = lambda seed=1234: map(
    lambda x: x / 4294967296,
    random_int_generator(seed)
)
