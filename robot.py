from robot_state_machine import RobotStates


class Robot:
    def __init__(self):
        self.state = RobotStates.USERNAME
        self.username = ''
        self.key = -1
        self.coordinates = None
        self.orientation = None

    def __str__(self):
        return "Robot info:\n\tName: " + self.username + ", state: " + self.state.name + ", coordinates: " + self.coordinates + ", orientation: " + self.orientation.name
