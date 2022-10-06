import socket as tcp
from time import sleep

pcHostName = tcp.gethostname()
hostIp = tcp.gethostbyname(pcHostName)
hostPort = 49252
serverAdress = (hostIp, hostPort)

robotIp = "198.162.0.1"
PORT = 2000 #todo: change this

print(f"""
pc name:    {pcHostName},
ip address: {hostIp},
pc port:    {hostPort}
""")

tcpSocket = tcp.socket(tcp.AF_INET, tcp.SOCK_STREAM)
tcpSocket.bind(serverAdress)
tcpSocket.listen(5)

x = 5.454
y = 1231.858
rot = 90
ori = 0

while True:
    print(f"[*] Started listening on :{hostIp}:{hostPort}")
    clientSocket, clientAddress = tcpSocket.accept()

    print(f"[*] Got connection from {clientAddress[0]}:{clientAddress[1]}")

    while True:
        data = clientSocket.recv(1024).decode()
        print(f"[*] Received {data} from the client")
        print("[*] Processing data")
        if(data == "hello server"):
            clientSocket.send("1".encode())
            print("[*] Reply sent: 1")
        elif(data=="close"):
            clientSocket.send("Goodbye".encode())
            print("[*] Reply sent: Goodbye")
            print("[*] Connection closed.")
            clientSocket.close()
            break
        elif(data == "quit"):
            clientSocket.send("Server stopped".encode())
            print("[*] Reply sent: Server Stopped")
            clientSocket.close()
            break
        elif(data=="getData"):
            coords = f"{x},{y},{rot},{ori}"
            print(coords)
            clientSocket.send(coords.encode())
            print(f"[*] Reply sent: {coords}")
    if(data == "quit"):
        break

print("[*] End of server program")