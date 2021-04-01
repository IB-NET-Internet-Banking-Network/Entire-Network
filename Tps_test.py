
from socket import*

TpsPortNumber = 9988

TpsServer = socket(AF_INET, SOCK_STREAM)

TpsServer.bind(('', TpsPortNumber))
TpsServer.listen(1)

print("Server is connected...")

while 1:
    ppInstance, ppAddress = TpsServer.accept()

    print("Connection established...")

    recvMsgFromPP = ppInstance.recv(2048)

    print("Received message...")
    print(recvMsgFromPP.decode())

    ppInstance.send("1".encode())



