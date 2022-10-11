import socket as tcp
from time import sleep

pcHostName = tcp.gethostname()
hostIp = tcp.gethostbyname(pcHostName)
HOSTPORT = 9000
serverAdress = (hostIp, HOSTPORT)

robotIp = "198.162.0.5"

print(f"""
pc name:    {pcHostName},
ip address: {hostIp},
pc port:    {HOSTPORT}
""")

tcpSocket = tcp.socket(tcp.AF_INET, tcp.SOCK_STREAM)
tcpSocket.bind(serverAdress)
tcpSocket.listen(5)


while True:
    print(f"\u001b[34m [*] \u001b[0m Started listening on :{hostIp}:{HOSTPORT}")
    clientSocket, (clientAddress,clientPort) = tcpSocket.accept()

    print(f"\u001b[34m [*] \u001b[0m Got connection from {clientAddress}:{clientPort}")

    while True:
        data = clientSocket.recv(1024).decode()
        print(f"\u001b[34m [*] \u001b[0m Received {data} from the client")
        print("\u001b[34m [*] \u001b[0m Processing data")
        if(data == "hello server"):
            clientSocket.send("1".encode())
            print("\u001b[34m [*] \u001b[0m Reply sent: 1")
        elif(data=="close"):
            clientSocket.send("Goodbye".encode())
            print("\u001b[34m [*] \u001b[0m Reply sent: Goodbye")
            print("\u001b[34m [*] \u001b[0m Connection closed.")
            clientSocket.close()
            break
        elif(data == "quit"):
            clientSocket.send("Server stopped".encode())
            print("\u001b[34m [*] \u001b[0m Reply sent: Server Stopped")
            clientSocket.close()
            break
        elif(data=="getData"):
            coords = f"{x},{y},{rot},{ori}"
            print(coords)
            clientSocket.send(coords.encode())
            print(f"\u001b[34m [*] \u001b[0m Reply sent: {coords}")
    if(data == "quit"):
        break

print("[*] End of server program")