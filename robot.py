from constants import Orientation, Side
from robot_constants import AuthenticationKeys, RobotAction, RobotStates


class Robot:
    def __init__(self):
        self.state = RobotStates.USERNAME
        self.username = ''
        self.key = -1
        self.coordinates = 'None'
        self.orientation = 'None'
        self.last_rotation = 'None'
        self.last_action = 'None'
        self.recharging = False

    def __str__(self):
        return "Robot info:\n\tName: " + self.username + ", state: " + str(self.state) + ", coordinates: " + str(self.coordinates) + ", orientation: " + str(self.orientation)


def calculate_hash(username, key, server_side):
    username_value = 0
    for i in range(len(username)):
        username_value += ord(username[i])

    key_name = "KEY_" + str(key)
    if server_side == Side.SERVER:
        auth_hash = AuthenticationKeys[key_name].value.server_key
    else:
        auth_hash = AuthenticationKeys[key_name].value.client_key

    return (username_value * 1000 + auth_hash) % 65536


def new_direction(current_orientation, searched_orientation):
    orientation_to_the_right = Orientation(
        (abs(current_orientation.value * 2)) % 3 * (-1 if current_orientation.value % 3 == 2 else 1))
    if current_orientation == searched_orientation:
        dir = RobotAction.GO_FORWARD
        new_orientation = current_orientation
    elif current_orientation == Orientation(searched_orientation.value*-1) or searched_orientation == orientation_to_the_right:
        dir = RobotAction.TURN_RIGHT
        new_orientation = orientation_to_the_right
    else:
        dir = RobotAction.TURN_LEFT
        new_orientation = Orientation(orientation_to_the_right.value * -1)

    return (new_orientation, dir)


def get_direction(current_coordinates, current_orientation):
    # could be more efficient, this one makes unnecesary turns
    should_go_forward = {
        Orientation.NORTH: current_coordinates.y < 0,
        Orientation.SOUTH: current_coordinates.y > 0,
        Orientation.EAST: current_coordinates.x < 0,
        Orientation.WEST: current_coordinates.x > 0,
    }.get(current_orientation, True)

    if should_go_forward:
        dir = RobotAction.GO_FORWARD
        new_orientation = current_orientation

    elif current_coordinates.x == 0:
        if current_coordinates.y == 0:
            dir = None
            new_orientation = current_orientation
        elif current_coordinates.y > 0:
            (new_orientation, dir) = new_direction(
                current_orientation, Orientation.SOUTH)
        else:
            (new_orientation, dir) = new_direction(
                current_orientation, Orientation.NORTH)

    else:
        if current_coordinates.x > 0:
            (new_orientation, dir) = new_direction(
                current_orientation, Orientation.WEST)
        else:
            (new_orientation, dir) = new_direction(
                current_orientation, Orientation.EAST)
    return (new_orientation, dir)


def get_direction_diagonalized(current_coordinates, current_orientation):
    # This method allows the robot to get to the end on the minimum number of moves but using a lot of turns
    if current_coordinates.x == 0:
        if current_coordinates.y == 0:
            dir = None
            new_orientation = current_orientation
        elif current_coordinates.y > 0:
            (new_orientation, dir) = new_direction(
                current_orientation, Orientation.SOUTH)
        else:
            (new_orientation, dir) = new_direction(
                current_orientation, Orientation.NORTH)
    elif current_coordinates.y == 0:
        if current_coordinates.x > 0:
            (new_orientation, dir) = new_direction(
                current_orientation, Orientation.WEST)
        else:
            (new_orientation, dir) = new_direction(
                current_orientation, Orientation.EAST)
    else:
        if abs(current_coordinates.x) > abs(current_coordinates.y):
            (new_orientation, dir) = new_direction(
                current_orientation, Orientation.WEST if current_coordinates.x > 0 else Orientation.EAST)
        else:
            (new_orientation, dir) = new_direction(
                current_orientation, Orientation.SOUTH if current_coordinates.y > 0 else Orientation.NORTH)

    return (new_orientation, dir)
