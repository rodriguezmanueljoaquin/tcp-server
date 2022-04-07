from enum import Enum
from constants import Orientation
from utils import Coordinates


class RobotStates(Enum):
    # Server waiting for:
    USERNAME = 0
    KEY = 1
    CONFIRMATION_KEY = 2
    FIRST_MOVE = 3
    ORIENTATION = 4
    COMMAND = 5
    DISCOVER_SECRET = 6
    WAIT_SECRET = 7
    DISCONNECTED = 8


class RobotDirection(Enum):
    FORWARD = 0
    RIGHT = 1
    LEFT = 2


class Robot:
    def __init__(self):
        self.state = RobotStates.USERNAME
        self.username = ''
        self.key = -1
        self.coordinates = 'None'
        self.orientation = 'None'

    def __str__(self):
        return "Robot info:\n\tName: " + self.username + ", state: " + self.state.name + ", coordinates: " + str(self.coordinates) + ", orientation: " + self.orientation.name


def new_direction(current_orientation, searched_orientation):
    orientation_to_the_right = Orientation(
        (abs(current_orientation.value * 2)) % 3 * (-1 if current_orientation.value % 3 == 2 else 1))
    if current_orientation.name == searched_orientation.name:
        dir = RobotDirection.FORWARD
        new_orientation = current_orientation
    elif current_orientation == Orientation(searched_orientation.value*-1) or searched_orientation == orientation_to_the_right:
        dir = RobotDirection.RIGHT
        new_orientation = orientation_to_the_right
    else:
        dir = RobotDirection.LEFT
        new_orientation = Orientation(orientation_to_the_right.value * -1)

    return (new_orientation, dir)


def get_direction(current_coordinates, current_orientation):
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
