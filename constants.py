
from enum import Enum

from utils import AuthenticationKeyPair


DELIMITER = "\a\b"


class Side(Enum):
    SERVER = 1
    CLIENT = 0


class Orientation(Enum):
    NORTH = 1
    SOUTH = -1
    EAST = 2
    WEST = -2


class AuthenticationKeys(Enum):
    KEY_0 = AuthenticationKeyPair(23019, 32037)
    KEY_1 = AuthenticationKeyPair(32037, 29295)
    KEY_2 = AuthenticationKeyPair(18789, 13603)
    KEY_3 = AuthenticationKeyPair(16443, 29533)
    KEY_4 = AuthenticationKeyPair(18189, 21952)
