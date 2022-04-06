import os
import socket
from robot import Robot
from robot_state_machine import new_robot_state_machine


def serve_client(socket):
    robot = Robot()

    while True:
        # recv gets sequence of bytes -> decoding into string

        data = socket.recv(1024).decode()
        if not data:
            # connection closed
            print("Robot disconnected ", robot)
            return

        print(data)
        data = sm.run(robot, data, socket)

        # TODO: No se puede sacar? sin esto se bloquea el recv
        # socket.send("ack".encode())

        if data is None:
            # robot reached an end state
            print("Robot disconnected ", robot)
            return


# socket creation: ip/tcp
l = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding the socket to this device, port number 6666
l.bind(('localhost', 6667))
l.listen(10)  # number of clients

sm = new_robot_state_machine()

print("Server waiting for clients...")
while True:

    # accept returns newly created socket and address of the client
    new_socket, address = l.accept()

    child_pid = os.fork()  # fork returns process id of the child - stored in the parent

    if child_pid != 0:  # we are in the parent thread
        new_socket.close()
        continue

    l.close()

    print(address)
    new_socket.settimeout(1000)
    try:
        serve_client(new_socket)
        new_socket.close()
        break  # child executes only one cycle

    except socket.timeout as e:  # if timeout occurs
        print("Timeout!")
        new_socket.close()
