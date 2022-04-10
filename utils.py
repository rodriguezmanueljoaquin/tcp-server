from constants import DELIMITER


class AuthenticationKeyPair:
    def __init__(self, server_key, client_key):
        self.server_key = server_key
        self.client_key = client_key


class Coordinates:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        if isinstance(other, Coordinates):
            return self.x == other.x and self.y == other.y

        return NotImplemented


def is_integer(str):
    possible_suffixes = ()
    for x in range(1, len(DELIMITER)):
        possible_suffixes += (DELIMITER[:x],)

    # +1 because of the possible sing(+ or -)
    if len(str) <= len(DELIMITER)-1 + 1 or str.endswith(possible_suffixes):
        return True
    if str[0] in ('-', '+'):
        return str[1:].isdigit()
    return str.isdigit()
