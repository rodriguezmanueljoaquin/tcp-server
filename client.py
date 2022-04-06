import socket
import sys
from time import sleep
import fileinput
from constants import DELIMITER

from robot_messages import Side, calculate_hash

# test client, not official

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', 6667))

username = "Meow!"
s.send((username+"\a\b").encode())
sleep(1)
print(s.recv(1024).decode())

key = 4
s.send((str(key)+"\a\b").encode())
sleep(1)
hash_received_plain = s.recv(1024).decode()
print(hash_received_plain)

hash_expected = calculate_hash(username, key, Side.SERVER)
hash_received = int(hash_received_plain.split(DELIMITER)[0])
print("Hash valido? ", hash_expected == hash_received)
hash = calculate_hash(username, key, Side.CLIENT)
s.send((str(hash)+"\a\b").encode())
sleep(1)
print(s.recv(1024).decode())

sleep(1)
print(s.recv(1024).decode())


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
