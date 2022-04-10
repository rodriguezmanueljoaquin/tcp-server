from constants import Orientation, Side, ServerMessages
from robot import RobotAction, get_direction, RobotStates, calculate_hash, new_direction
import robot_constants
from utils import Coordinates


def username_transition(robot, msg, client_socket):
    robot.state = RobotStates.KEY
    robot.username = msg
    client_socket.send(ServerMessages.KEY_REQUEST.value.encode())


def key_transition(robot, msg, client_socket):
    key = int(msg)
    if key < robot_constants.KEY_MIN_VALUE or key > robot_constants.KEY_MAX_VALUE:
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

    if hash_received > robot_constants.HASH_MAX_VALUE or hash_received < robot_constants.HASH_MIN_VALUE:
        client_socket.send(
            ServerMessages.SYNTAX_ERROR.value.encode())
        robot.state = RobotStates.LOGOUT
        return

    if hash_expected != hash_received:
        print("Login failed for ", robot, " hash expected: ",
              hash_expected, " hash received: ", hash_received)
        client_socket.send(
            ServerMessages.LOGIN_FAILED.value.encode())
        return

    client_socket.send(ServerMessages.OK.value.encode())
    robot.state = RobotStates.FIRST_MOVE
    client_socket.send(ServerMessages.MOVE.value.encode())
    return


def get_positions(msg):
    positions_str = msg.split(" ")[1:]
    return Coordinates(*positions_str)


def first_move_transition(robot, msg, client_socket):
    robot.coordinates = get_positions(msg)
    client_socket.send(ServerMessages.MOVE.value.encode())
    robot.state = RobotStates.ORIENTATION
    return


def execute_next_move(robot, client_socket):
    (new_orientation, rotate_to) = get_direction(
        robot.coordinates, robot.orientation)
    robot.orientation = new_orientation

    if rotate_to is None:
        # reached 0,0
        client_socket.send(ServerMessages.PICK_UP.value.encode())
        robot.state = RobotStates.WAIT_SECRET
    else:
        robot.last_rotation = rotate_to
        send_action(robot, rotate_to, client_socket)


def orientation_transition(robot, msg, client_socket):
    current_coordinates = get_positions(msg)

    orientation_value = (robot.coordinates.x - current_coordinates.x) * \
        2 + (robot.coordinates.y - current_coordinates.y)
    robot.orientation = {
        -2: Orientation.EAST,
        2: Orientation.WEST,
        1: Orientation.SOUTH,
        -1: Orientation.NORTH
    }.get(orientation_value, None)
    robot.coordinates = current_coordinates

    if not robot.orientation:
        client_socket.send(
            ServerMessages.TURN_RIGHT.value.encode())
        robot.state = RobotStates.FIRST_MOVE
        return

    execute_next_move(robot, client_socket)
    robot.state = RobotStates.COMMAND
    return


def send_action(robot, action, client_socket):
    if action == RobotAction.GO_FORWARD:
        client_socket.send(ServerMessages.MOVE.value.encode())
        robot.last_action = RobotAction.GO_FORWARD
    elif action == RobotAction.TURN_RIGHT:
        client_socket.send(ServerMessages.TURN_RIGHT.value.encode())
        robot.last_action = RobotAction.TURN_RIGHT
    else:
        client_socket.send(ServerMessages.TURN_LEFT.value.encode())
        robot.last_action = RobotAction.TURN_LEFT


def command_transtition(robot, msg, client_socket):
    current_coordinates = get_positions(msg)

    if current_coordinates == robot.coordinates and robot.last_action == RobotAction.GO_FORWARD:
        if robot.coordinates.x == 0 or robot.coordinates.y == 0:
            # requires double forced rotation
            dodge_rotation(robot, client_socket, True)
        else:
            dodge_rotation(robot, client_socket, False)
    else:
        robot.coordinates = current_coordinates
        execute_next_move(robot, client_socket)

    return


def dodge_rotation(robot, client_socket, double_rotation):
    if robot.orientation == Orientation.NORTH or robot.orientation == Orientation.SOUTH:
        (new_orientation, rotate_to) = new_direction(robot.orientation,
                                                     Orientation.EAST if robot.coordinates.x < 0 else Orientation.WEST)
    else:
        (new_orientation, rotate_to) = new_direction(robot.orientation,
                                                     Orientation.NORTH if robot.coordinates.y < 0 else Orientation.SOUTH)

    robot.orientation = new_orientation
    robot.last_rotation = rotate_to
    send_action(robot, rotate_to, client_socket)
    if double_rotation:
        robot.state = RobotStates.DODGE_FIRST_FORWARD
    else:
        robot.state = RobotStates.DODGE_SECOND_FORWARD


def dodge_transition(robot, msg, client_socket):
    robot.coordinates = get_positions(msg)
    if robot.state == RobotStates.DODGE_FIRST_FORWARD:
        send_action(robot, RobotAction.GO_FORWARD, client_socket)
        robot.state = RobotStates.DODGE_SECOND_ROTATION

    elif robot.state == RobotStates.DODGE_SECOND_ROTATION:
        rotate_to = RobotAction(robot.last_rotation.value * -1)

        send_action(robot, rotate_to, client_socket)
        robot.last_rotation = rotate_to
        robot.state = RobotStates.DODGE_SECOND_FORWARD
        orientation_to_the_right = Orientation(
            (abs(robot.orientation.value * 2)) % 3 * (-1 if robot.orientation.value % 3 == 2 else 1))
        robot.orientation = Orientation(
            orientation_to_the_right.value * (1 if rotate_to == RobotAction.TURN_RIGHT else -1))

    elif robot.state == RobotStates.DODGE_SECOND_FORWARD:
        send_action(robot, RobotAction.GO_FORWARD, client_socket)
        robot.state = RobotStates.COMMAND

    else:
        print("Invalid state for dodge transition")
        client_socket.send(
            ServerMessages.LOGIC_ERROR.value.encode())
        robot.state = RobotStates.LOGOUT

    return


def wait_secret_transition(robot, msg, client_socket):
    print("Secret of robot ", robot.username, " is: ", msg)
    client_socket.send(ServerMessages.LOGOUT.value.encode())
    robot.state = RobotStates.LOGOUT
    return
