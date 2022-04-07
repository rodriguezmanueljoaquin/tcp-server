from enum import Enum

from utils import AuthenticationKeyPair


class RobotStates(Enum):
    # Server waiting for:
    USERNAME = 0
    KEY = 1
    CONFIRMATION_KEY = 2
    FIRST_MOVE = 3
    ORIENTATION = 4
    COMMAND = 5
    WAIT_SECRET = 6
    LOGOUT = 7


class RobotDirection(Enum):
    FORWARD = 0
    RIGHT = 1
    LEFT = 2


class RobotTimes(Enum):
    TIMEOUT = 1
    TIMEOUT_RECHARGING = 5


class RobotMessageRestriction:
    def __init__(self, max_length, min_value=-1, max_value=-1):
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value


class RobotMessagesRestrictions(Enum):
    USERNAME = RobotMessageRestriction(18)
    KEY_ID = RobotMessageRestriction(-1, 0, 4)
    CONFIRMATION = RobotMessageRestriction(5)
    OK = RobotMessageRestriction(2)
    RECHARGING = RobotMessageRestriction(0)
    FULL_POWER = RobotMessageRestriction(0)
    MESSAGE = RobotMessageRestriction(100)


class AuthenticationKeys(Enum):
    KEY_0 = AuthenticationKeyPair(23019, 32037)
    KEY_1 = AuthenticationKeyPair(32037, 29295)
    KEY_2 = AuthenticationKeyPair(18789, 13603)
    KEY_3 = AuthenticationKeyPair(16443, 29533)
    KEY_4 = AuthenticationKeyPair(18189, 21952)
