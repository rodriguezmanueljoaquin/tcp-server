from time import sleep
from enum import Enum

from constants import DELIMITER, Coordinates, Orientation
from robot_messages import RobotMessagesRestrictions, ServerMessages, Side, calculate_hash


class RobotStates(Enum):
    # Server waiting for:
    USERNAME: int = 0
    KEY: int = 1
    CONFIRMATION_KEY: int = 2
    DISCOVER: int = 3
    ORIENTATION: int = 4
    COMMAND: int = 5
    END: int = 6


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

        if DELIMITER not in msg:
            print("DELIMITER NOT IN: " + msg)
            # not ready to be processed
            return msg

        tokens = msg.split(DELIMITER)
        handler = self.handlers[robot.state]
        handler(robot, tokens[0], client_socket)
        print("state: ", robot.state)
        if robot.state in self.end_states:
            print("Reached end state")
            return None

        return "".join(tokens[1:])


def username_transition(robot, username, client_socket):
    if len(username) > RobotMessagesRestrictions.USERNAME.value.max_length:
        client_socket.send(ServerMessages.SERVER_SYNTAX_ERROR.value.encode())
        return
    else:
        robot.state = RobotStates.KEY
        robot.username = username
        client_socket.send(ServerMessages.SERVER_KEY_REQUEST.value.encode())


def key_transition(robot, msg, client_socket):
    key = int(msg)
    if key < RobotMessagesRestrictions.KEY_ID.value.min_value or key > RobotMessagesRestrictions.KEY_ID.value.max_value:
        print("Key out of range for ", robot)
        client_socket.send(
            ServerMessages.SERVER_KEY_OUT_OF_RANGE_ERROR.value.encode())
        return

    robot.key = key
    robot.state = RobotStates.CONFIRMATION_KEY
    hash = calculate_hash(robot.username, key, Side.SERVER)
    client_socket.send(
        (str(hash) + ServerMessages.SERVER_CONFIRMATION.value).encode())


def confirmation_key_transition(robot, msg, client_socket):
    hash_expected = calculate_hash(robot.username, robot.key, Side.CLIENT)
    hash_received = int(msg)
    if hash_expected != hash_received:
        print("Login failed for ", robot)
        client_socket.send(
            ServerMessages.SERVER_LOGIN_FAILED.value.encode())
        return None

    robot.state = RobotStates.DISCOVER
    client_socket.send(ServerMessages.SERVER_OK.value.encode())
    sleep(5)
    client_socket.send(ServerMessages.SERVER_MOVE.value.encode())


def discover_transition(robot, msg, client_socket):
    positions = msg.split(" ")[1:]
    robot.coordinates = Coordinates(positions)
    client_socket.send(ServerMessages.SERVER_MOVE.value.encode())
    robot.state = RobotStates.ORIENTATION


def orientation_transition(robot, msg, client_socket):
    new_coordinates = Coordinates(msg.split(" ")[1:])
    orientation_value = (robot.coordinates.x - new_coordinates.x) * \
        2 + (robot.coordinates.y - new_coordinates.y)
    robot.orientation = {
        -2: Orientation.NORTH,
        2: Orientation.SOUTH,
        1: Orientation.EAST,
        -1: Orientation.WEST
    }.get(orientation_value, None)
    robot.coordinates = new_coordinates

    if not robot.orientation:
        client_socket.send(
            ServerMessages.SERVER_TURN_RIGHT.value.encode())
        return

    robot.state = RobotStates.COMMAND


def turn_to(current_orientation, searched_orientation):
    orientation_to_the_right = Orientation(
        (abs(current_orientation.value * 2)) % 3 * (-1 if current_orientation.value %2 == 0 else 1))
    print(orientation_to_the_right)
    if current_orientation == searched_orientation:
        turn = None
    elif current_orientation == Orientation(searched_orientation.value*-1) or searched_orientation == orientation_to_the_right:
        turn = "RIGHT"
    else:
        turn = "LEFT"

    return turn


print(turn_to(Orientation.NORTH, Orientation.EAST))
print(turn_to(Orientation.EAST, Orientation.SOUTH))
print(turn_to(Orientation.SOUTH, Orientation.WEST))
print(turn_to(Orientation.WEST, Orientation.NORTH))


def command_transtition(robot, msg, client_socket):
    new_coordinates = Coordinates(msg.split(" ")[1:])
    if new_coordinates == robot.coordinates:
        client_socket.send(ServerMessages.SERVER_TURN_RIGHT.value.encode())
        return

    robot.coordinates = new_coordinates
    if robot.coordinates.x == 0:
        if robot.coordinates.y == 0:
            robot.state = RobotStates.END
            return
        elif robot.coordinates.y > 0:
            # hacia el sur
            turn = turn_to(robot.orientation, Orientation.SOUTH)
        else:
            # hacia el norte
            turn = turn_to(robot.orientation, Orientation.NORTH)
    else:
        if robot.coordinates.x > 0:
            # hacia el oeste
            turn = turn_to(robot.orientation, Orientation.WEST)
        else:
            # hacia el este
            turn = turn_to(robot.orientation, Orientation.EAST)

    print(turn)


def turn_to(current_orientation, searched_orientation):
    if current_orientation == searched_orientation:
        return None

    return {
        "RIGHT": 2,
        2: Orientation.SOUTH,
        1: Orientation.EAST,
        -1: Orientation.WEST
    }.get(current_orientation - searched_orientation, None)


def new_robot_state_machine():
    sm = RobotStateMachine()
    sm.add_state(RobotStates.USERNAME, username_transition)
    sm.add_state(RobotStates.KEY, key_transition)
    sm.add_state(RobotStates.CONFIRMATION_KEY, confirmation_key_transition)
    sm.add_state(RobotStates.DISCOVER, discover_transition)
    sm.add_state(RobotStates.ORIENTATION, orientation_transition)
    sm.add_state(RobotStates.COMMAND, command_transtition)

    sm.set_start_state(RobotStates.USERNAME)

    sm.set_end_state(RobotStates.END)

    return sm
