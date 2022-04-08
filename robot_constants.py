from enum import Enum

from utils import AuthenticationKeyPair


USERNAME_MAX_LENGTH = 18
MESSAGE_MAX_LENGTH = 98
KEY_MIN_VALUE = 0
KEY_MAX_VALUE = 4
HASH_MIN_VALUE = 0
HASH_MAX_VALUE = 2 ** 16
RECHARGING_STR = "RECHARGING"
FULLPOWER_STR = "FULL POWER"
TIMEOUT = 1
TIMEOUT_RECHARGING = 5


class RobotStates(Enum):
    # Server waiting for:
    USERNAME = 0
    KEY = 1
    CONFIRMATION_KEY = 2
    FIRST_MOVE = 3
    ORIENTATION = 4
    COMMAND = 5
    DODGE_FIRST_FORWARD = 6
    DODGE_SECOND_ROTATION = 7
    DODGE_SECOND_FORWARD = 8
    WAIT_SECRET = 9
    LOGOUT = 10
    RCHARGING = 11


class RobotAction(Enum):
    GO_FORWARD = 0
    TURN_RIGHT = 1
    TURN_LEFT = -1


class RobotMessageRestriction:
    def __init__(self, max_length, min_value=-1, max_value=-1):
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value


class AuthenticationKeys(Enum):
    KEY_0 = AuthenticationKeyPair(23019, 32037)
    KEY_1 = AuthenticationKeyPair(32037, 29295)
    KEY_2 = AuthenticationKeyPair(18789, 13603)
    KEY_3 = AuthenticationKeyPair(16443, 29533)
    KEY_4 = AuthenticationKeyPair(18189, 21952)
