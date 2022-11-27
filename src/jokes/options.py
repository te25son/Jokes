from enum import Enum


class Categories(Enum):
    ANY = "any"
    MISC = "misc"
    PROGRAMMING = "programming"
    DARK = "dark"
    PUN = "pun"
    SPOOKY = "spooky"
    CHRISTMAS = "christmas"


class Types(Enum):
    SINGLE = "single"
    TWOPART = "twopart"


class Flags(Enum):
    NSFW = "nsfw"
    RELIGIOUS = "religious"
    POLITICAL = "political"
    RACIST = "racist"
    SEXIST = "sexist"
    EXPLICIT = "explicit"


class Languages(Enum):
    CS = "cs"
    DE = "de"
    EN = "en"
    ES = "es"
    FR = "fr"
    PT = "pt"
