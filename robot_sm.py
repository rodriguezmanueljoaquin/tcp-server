from constants import DELIMITER,  ServerMessages
from robot import RobotStates
import robot_constants
import robot_sm_validators
import robot_sm_handlers


class RobotStateMachine:
    def __init__(self):
        self.handlers = {}
        self.validators = {}
        self.start_state = None
        self.end_states = []

    def add_state(self, id, validator, handler, end_state=0):
        self.id = id
        self.validators[id] = validator
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

        while True:

            tokens = msg.split(DELIMITER)
            processed = True
            if len(tokens[0]) > robot_constants.MESSAGE_MAX_LENGTH:
                client_socket.send(ServerMessages.SYNTAX_ERROR.value.encode())
                return None

            if tokens[0] == robot_constants.RECHARGING_STR:
                robot.recharging = True
                client_socket.settimeout(robot_constants.TIMEOUT_RECHARGING)

            elif tokens[0] == robot_constants.FULLPOWER_STR:
                if not robot.recharging:
                    client_socket.send(
                        ServerMessages.LOGIC_ERROR.value.encode())
                    return None
                robot.recharging = False
                client_socket.settimeout(robot_constants.TIMEOUT)

            elif robot.recharging:
                client_socket.send(ServerMessages.LOGIC_ERROR.value.encode())
                return None

            else:
                processed = self.validators[robot.state](
                    robot, tokens[0], client_socket, len(tokens) > 1)
                if processed == robot_constants.VALID_MSG:
                    self.handlers[robot.state](
                        robot, tokens[0], client_socket)

                if robot.state in self.end_states:
                    print("Reached end state")
                    return None

            msg = DELIMITER.join(
                tokens[(1 if processed == robot_constants.VALID_MSG else 0):])

            #print(robot.id, robot.coordinates, robot.orientation, robot.last_action)

            if not DELIMITER in msg:
                # to simulate a Do while statement, which allows us to detect wrong messages prior receiving the DELIMITER
                break

        return msg


def new_robot_state_machine():
    sm = RobotStateMachine()
    sm.add_state(RobotStates.USERNAME,
                 robot_sm_validators.username_validation, 
                 robot_sm_handlers.username_transition)

    sm.add_state(RobotStates.KEY,
                 robot_sm_validators.key_validation, 
                 robot_sm_handlers.key_transition)

    sm.add_state(RobotStates.CONFIRMATION_KEY,
                 robot_sm_validators.confirmation_key_validation, 
                 robot_sm_handlers.confirmation_key_transition)

    sm.add_state(RobotStates.FIRST_MOVE,
                 robot_sm_validators.get_positions_validation, 
                 robot_sm_handlers.first_move_transition)

    sm.add_state(RobotStates.ORIENTATION,
                 robot_sm_validators.get_positions_validation, 
                 robot_sm_handlers.orientation_transition)

    sm.add_state(RobotStates.COMMAND,
                 robot_sm_validators.get_positions_validation, 
                 robot_sm_handlers.command_transtition)

    sm.add_state(RobotStates.DODGE_FIRST_FORWARD,
                 robot_sm_validators.get_positions_validation, 
                 robot_sm_handlers.dodge_transition)

    sm.add_state(RobotStates.DODGE_SECOND_ROTATION,
                 robot_sm_validators.get_positions_validation, 
                 robot_sm_handlers.dodge_transition)

    sm.add_state(RobotStates.DODGE_SECOND_FORWARD,
                 robot_sm_validators.get_positions_validation, 
                 robot_sm_handlers.dodge_transition)

    sm.add_state(RobotStates.WAIT_SECRET,
                 robot_sm_validators.wait_secret_validation, 
                 robot_sm_handlers.wait_secret_transition)

    sm.set_start_state(RobotStates.USERNAME)

    sm.set_end_state(RobotStates.LOGOUT)

    return sm
