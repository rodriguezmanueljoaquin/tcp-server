from enum import Enum

from constants import DELIMITER, AuthenticationKeys


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


class ServerMessages(Enum):
    SERVER_KEY_REQUEST = "107 KEY REQUEST" + DELIMITER
    SERVER_CONFIRMATION = "" + DELIMITER
    SERVER_MOVE = "102 MOVE" + DELIMITER
    SERVER_TURN_LEFT = "103 TURN LEFT" + DELIMITER
    SERVER_TURN_RIGHT = "104 TURN RIGHT" + DELIMITER
    SERVER_PICK_UP = "105 GET MESSAGE" + DELIMITER
    SERVER_LOGOUT = "106 LOGOUT" + DELIMITER
    SERVER_OK = "200 OK" + DELIMITER
    SERVER_LOGIN_FAILED = "300 LOGIN FAILED" + DELIMITER
    SERVER_SYNTAX_ERROR = "301 SYNTAX ERROR" + DELIMITER
    SERVER_LOGIC_ERROR = "302 LOGIC ERROR" + DELIMITER
    SERVER_KEY_OUT_OF_RANGE_ERROR = "303 KEY OUT OF RANGE" + DELIMITER


def calculate_hash(username, key, server_side):
    username_value = 0
    for i in range(len(username)):
        username_value += ord(username[i])

    if server_side:
        auth_hash = AuthenticationKeys.KEY_0.value.server_key
    else:
        auth_hash = AuthenticationKeys.KEY_0.value.client_key
    return (username_value * 1000 + auth_hash) % 65536
