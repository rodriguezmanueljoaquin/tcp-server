from enum import Enum

DELIMITER = "\a\b"


class AuthenticationKeyPair:
    def __init__(self, server_key, client_key):
        self.server_key = server_key
        self.client_key = client_key


class Orientation(Enum):
    NORTH = 1
    SOUTH = -1
    EAST = 2
    WEST = -2


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class AuthenticationKeys(Enum):
    KEY_0 = AuthenticationKeyPair(23019, 32037)
    KEY_1 = AuthenticationKeyPair(32037, 29295)
    KEY_2 = AuthenticationKeyPair(18789, 13603)
    KEY_3 = AuthenticationKeyPair(16443, 29533)
    KEY_4 = AuthenticationKeyPair(18189, 21952)
