from time import sleep

from constants import DELIMITER, Orientation, Side, ServerMessages
from robot import RobotDirection, get_direction, RobotStates, calculate_hash
from robot_constants import RobotMessagesRestrictions
from utils import Coordinates


class RobotStateMachine:
    def __init__(self):
        self.handlers = {}
        self.start_state = None
        self.end_states = []

    def add_state(self, id, handler, end_state=0):
        self.id = id
        self.handlers[id] = handler
        if end_state:
            self.end_states.append(id)

    def set_start_state(self, id):
        self.start_state = id

    def set_end_state(self, id):
        self.end_states.append(id)

    def run(self, robot, msg, client_socket):
        if msg is None:
            return msg
        while DELIMITER in msg:

            tokens = msg.split(DELIMITER)
            handler = self.handlers[robot.state]
            handler(robot, tokens[0], client_socket)

            if robot.state in self.end_states:
                print("Reached end state")
                return None

            msg = DELIMITER.join(tokens[1:])

        return msg


def username_transition(robot, username, client_socket):
    if len(username) > RobotMessagesRestrictions.USERNAME.value.max_length:
        client_socket.send(ServerMessages.SYNTAX_ERROR.value.encode())
        return
    else:
        robot.state = RobotStates.KEY
        robot.username = username
        client_socket.send(ServerMessages.KEY_REQUEST.value.encode())


def key_transition(robot, msg, client_socket):
    key = int(msg)
    if key < RobotMessagesRestrictions.KEY_ID.value.min_value or key > RobotMessagesRestrictions.KEY_ID.value.max_value:
        print("Key out of range for ", robot)
        client_socket.send(
            ServerMessages.KEY_OUT_OF_RANGE_ERROR.value.encode())
        return

    robot.key = key
    robot.state = RobotStates.CONFIRMATION_KEY
    hash = calculate_hash(robot.username, key, Side.SERVER)
    client_socket.send(
        (str(hash) + ServerMessages.CONFIRMATION.value).encode())


def confirmation_key_transition(robot, msg, client_socket):
    hash_expected = calculate_hash(robot.username, robot.key, Side.CLIENT)
    hash_received = int(msg)
    if hash_expected != hash_received:
        print("Login failed for ", robot, " hash expected: ", hash_expected, " hash received: ", hash_received)
        client_socket.send(
            ServerMessages.LOGIN_FAILED.value.encode())
        return None

    client_socket.send(ServerMessages.OK.value.encode())
    robot.state = RobotStates.FIRST_MOVE
    client_socket.send(ServerMessages.MOVE.value.encode())


def first_move_transition(robot, msg, client_socket):
    positions = [*map(lambda x: int(x), msg.split(" ")[1:])]
    robot.coordinates = Coordinates(*positions)
    client_socket.send(ServerMessages.MOVE.value.encode())
    robot.state = RobotStates.ORIENTATION


def orientation_transition(robot, msg, client_socket):
    new_coordinates = Coordinates(*msg.split(" ")[1:])
    orientation_value = (robot.coordinates.x - new_coordinates.x) * \
        2 + (robot.coordinates.y - new_coordinates.y)
    robot.orientation = {
        -2: Orientation.EAST,
        2: Orientation.WEST,
        1: Orientation.SOUTH,
        -1: Orientation.NORTH
    }.get(orientation_value, None)
    robot.coordinates = new_coordinates

    if not robot.orientation:
        client_socket.send(
            ServerMessages.TURN_RIGHT.value.encode())
        return

    robot.state = RobotStates.COMMAND
    command_transtition(robot, msg, client_socket)


def command_transtition(robot, msg, client_socket):

    current_coordinates = Coordinates(*msg.split(" ")[1:])
    print(str(current_coordinates), robot.orientation)
    if current_coordinates == robot.coordinates:
        # TODO: should rotate to the correct side and go forward
        client_socket.send(ServerMessages.TURN_RIGHT.value.encode())
        return

    robot.coordinates = current_coordinates
    (new_orientation, dir) = get_direction(
        robot.coordinates, robot.orientation)
    robot.orientation = new_orientation
    if dir is None:
        # reached 0,0
        client_socket.send(ServerMessages.PICK_UP.value.encode())
        robot.state = RobotStates.WAIT_SECRET
    elif dir == RobotDirection.FORWARD:
        client_socket.send(ServerMessages.MOVE.value.encode())
    elif dir == RobotDirection.RIGHT:
        client_socket.send(ServerMessages.TURN_RIGHT.value.encode())
    else:
        client_socket.send(ServerMessages.TURN_LEFT.value.encode())



def wait_secret_transition(robot, msg, client_socket):
    print("Secret of robot ", robot.username, " is: ", msg)
    client_socket.send(ServerMessages.LOGOUT.value.encode())
    robot.state = RobotStates.LOGOUT


def new_robot_state_machine():
    sm = RobotStateMachine()
    sm.add_state(RobotStates.USERNAME, username_transition)
    sm.add_state(RobotStates.KEY, key_transition)
    sm.add_state(RobotStates.CONFIRMATION_KEY, confirmation_key_transition)
    sm.add_state(RobotStates.FIRST_MOVE, first_move_transition)
    sm.add_state(RobotStates.ORIENTATION, orientation_transition)
    sm.add_state(RobotStates.COMMAND, command_transtition)
    sm.add_state(RobotStates.WAIT_SECRET, wait_secret_transition)

    sm.set_start_state(RobotStates.USERNAME)

    sm.set_end_state(RobotStates.LOGOUT)

    return sm
