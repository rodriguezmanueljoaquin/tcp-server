# TCP-Server assignment for Computer Networks at CTU (Czech Technical University)
## Server for control of robot clients, implementation in Python

## Authors
- [Manuel Joaquín Rodríguez](https://github.com/rodriguezmanueljoaquin)

## About the project
The task consists on creating a server for automatic control of remote robots. Robots will authenticate to the server and then server directs them to the origin of the coordinate system. For testing purposes each robot starts at the random coordinates and its target location is always located on the coordinate [0,0]. The robot should reach that target coordinate avoiding obstacles and pick the secret message, which can be found only on that spot. Server is able to navigate several robots at once and implements communication protocol without errors.

## Dependencies
- Python 2.7.18

## How to run the project
To start the server, from the `server.py` directory run:
```
python3 server.py -p PORT -a ADDRESS
```
`PORT` is an optional argument, it defaults to port `6667` and it is the port where the server will be listening for clients.
`ADDRESS` is an optional argument, it defaults to `localhost` and it is the port where the server will be listening for clients.

## Tester
A tester is provided by the course, which can be found on: https://drive.google.com/drive/folders/1QzPyzZeLNWZhjtbaTGehyNu-zgHcInta?usp=sharing

In order tu run it, from the directory where the executable is use: 
```
./tester 6667 localhost
```