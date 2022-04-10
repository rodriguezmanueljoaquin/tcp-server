from constants import DELIMITER, ServerMessages
from robot import RobotStates
import robot_constants
from utils import is_integer


def wait_secret_validation(robot, msg, client_socket, is_msg_completed):
    return robot_constants.VALID_MSG if is_msg_completed else robot_constants.NOT_COMPLETED_MSG


def get_positions_validation(robot, msg, client_socket, is_msg_completed):
    tokens = msg.split(" ")
    if len(tokens) < 3:
        return robot_constants.NOT_COMPLETED_MSG

    positions_str = tokens[1:]
    if len(positions_str) > 2 or not is_integer(positions_str[0]) or not is_integer(positions_str[1]):
        client_socket.send(ServerMessages.SYNTAX_ERROR.value.encode())
        robot.state = RobotStates.LOGOUT
        return robot_constants.INVALID_MSG

    return robot_constants.VALID_MSG if is_msg_completed else robot_constants.NOT_COMPLETED_MSG


def confirmation_key_validation(robot, msg, client_socket, is_msg_completed):
    if len(msg) > robot_constants.HASH_MAX_VALUE + (len(DELIMITER)-1 if not is_msg_completed else 0) \
            or not is_integer(str(msg)):
        print("msg:", msg, len(msg), robot_constants.HASH_MAX_VALUE +
              (len(DELIMITER)-1 if not is_msg_completed else 0))
        client_socket.send(ServerMessages.SYNTAX_ERROR.value.encode())
        robot.state = RobotStates.LOGOUT
        return robot_constants.INVALID_MSG
    return robot_constants.VALID_MSG if is_msg_completed else robot_constants.NOT_COMPLETED_MSG


def key_validation(robot, msg, client_socket, is_msg_completed):
    if len(msg) > robot_constants.KEY_MAX_VALUE + (len(DELIMITER)-1 if not is_msg_completed else 0) or not is_integer(str(msg)):
        client_socket.send(ServerMessages.SYNTAX_ERROR.value.encode())
        robot.state = RobotStates.LOGOUT
        return robot_constants.INVALID_MSG

    return robot_constants.VALID_MSG if is_msg_completed else robot_constants.NOT_COMPLETED_MSG


def username_validation(robot, msg, client_socket, is_msg_completed):
    if len(msg) > robot_constants.USERNAME_MAX_LENGTH + (len(DELIMITER)-1 if not is_msg_completed else 0):
        client_socket.send(ServerMessages.SYNTAX_ERROR.value.encode())
        robot.state = RobotStates.LOGOUT
        return robot_constants.INVALID_MSG
    return robot_constants.VALID_MSG if is_msg_completed else robot_constants.NOT_COMPLETED_MSG
