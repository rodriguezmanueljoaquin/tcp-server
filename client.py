import socket
import sys
from time import sleep
import fileinput
from constants import Orientation, Side, DELIMITER
from robot import Robot

from robot_constants import calculate_hash
from utils import Coordinates


def orientation_change(orientation, turn):
    if turn == "LEFT":
        return Orientation(
            (abs(orientation.value * 2)) % 3 * (1 if orientation.value % 3 == 2 else -11))
    else:
        return Orientation(
            (abs(orientation.value * 2)) % 3 * (-1 if orientation.value % 3 == 2 else 1))


def move_forward(old_coordinates, orientation):
    # could be better
    if orientation == orientation.NORTH:
        new_coordinates = Coordinates(old_coordinates.x, old_coordinates.y + 1)
    elif orientation == orientation.SOUTH:
        new_coordinates = Coordinates(old_coordinates.x, old_coordinates.y - 1)
    elif orientation == orientation.EAST:
        new_coordinates = Coordinates(old_coordinates.x + 1, old_coordinates.y)
    elif orientation == orientation.WEST:
        new_coordinates = Coordinates(old_coordinates.x - 1, old_coordinates.y)
    else:
        print("ERROR ON ORIENTATION")
        return

    return new_coordinates


# test client, not official
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
robot = Robot()
robot.username = "Meow!"
robot.key = 4
robot.coordinates = Coordinates(-2, 5)
robot.orientation = Orientation.SOUTH

s.connect(('localhost', 6667))

s.send((robot.username+"\a\b").encode())
sleep(1)
print(s.recv(1024).decode())

s.send((str(robot.key)+"\a\b").encode())
sleep(1)
hash_received_plain = s.recv(1024).decode()
print(hash_received_plain)

hash_expected = calculate_hash(robot.username, robot.key, Side.SERVER)
hash_received = int(hash_received_plain.split(DELIMITER)[0])
print("Hash valido? " + str(hash_expected == hash_received))
hash = calculate_hash(robot.username, robot.key, Side.CLIENT)
s.send((str(hash)+"\a\b").encode())
sleep(1)
print(s.recv(1024).decode())

sleep(1)
print(s.recv(1024).decode())

while True:
    s.send("OK " + str(robot.coordinates.x) + " " +
           str(robot.coordinates.y) + "\a\b".encode())
    sleep(1)
    msg = s.recv(1024).decode()
    print(msg)
    if "102" in msg:
        robot.coordinates = move_forward(robot.coordinates, robot.orientation)
    elif "103" in msg:
        robot.orientation = orientation_change(robot.orientation, "LEFT")
    elif "104" in msg:
        robot.orientation = orientation_change(robot.orientation, "RIGHT")
    else:
        print("Unknown command received")
        break
    sleep(1)


s.close()
pass

# testing with input
for line in fileinput.input():
    line = line[:line.find("\n")]
    if line == 'fin':
        print("\\a\\b sended")
        s.send("\a\b".encode())
    else:
        s.send(line.encode())

    print(s.recv(1024).decode())

s.close()
