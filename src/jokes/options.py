import typing

from enum import Enum, auto
from dataclasses import dataclass


class Category(Enum):
    ANY = auto()
    MISC = auto()
    PROGRAMMING = auto()
    DARK = auto()
    PUN = auto()
    SPOOKY = auto()
    CHRISTMAS = auto()


class Type(Enum):
    SINGLE = auto()
    TWOPART = auto()


class Flag(Enum):
    NSFW = auto()
    RELIGIOUS = auto()
    POLITICAL = auto()
    RACIST = auto()
    SEXIST = auto()
    EXPLICIT = auto()


@dataclass
class OptionData:
    category: str
    type: str
    flags: list[str]


def as_list(klass: typing.Type[Enum]) -> list[str]:
    return [name for name, _ in klass.__members__.items()]