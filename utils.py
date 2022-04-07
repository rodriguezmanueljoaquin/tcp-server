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