import socket as tcp
from time import sleep

ip = "192.168.0.10"
PORT = 42520
sockett =  tcp.socket(tcp.AF_INET,tcp.SOCK_STREAM)
while True:
    sockett.connect((ip,PORT))
    while True:
        sockett.send("Q1")
        sleep(0.185)
        data = sockett.recv(1024)
        print(data)

        sleep(2)
        sockett.send("Q1")
        sleep(0.185)
        data = sockett.recv(1024)
        print(data)