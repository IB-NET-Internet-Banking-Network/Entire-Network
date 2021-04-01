
from socket import*

# CIF Customer Information file
# It maaps between the Card info to the Bank information
global CIF_number
CIF_number={
    "1001 0110 2002 0011":"98765432011",
    "1001 0110 2002 0026":"98765432026",
    "1001 0110 2002 0006":"98765432006"
}

global accountDetails
accountDetails={
    "98765432011":["00000000011", "RBIS0PFMS01"],
    "98765432026":["00000000026", "RBIS0PFMS01"],
    "98765432006":["00000000006", "RBIS0PFMS01"],
}
# function for converting the binary message into list
# Input is receved message from payment gateway
# output is full message in list
def give_list(recvMessage):
	recvMessage = recvMessage.decode()

	recvMessage2 = eval(recvMessage)

	return recvMessage2



TpsPortNumber = 9988

TpsServer = socket(AF_INET, SOCK_STREAM)

TpsServer.bind(('', TpsPortNumber))
TpsServer.listen(1)

print("Server is connected...")

while 1:
    ppInstance, ppAddress = TpsServer.accept()

    print("Connection established...")

    recvMsgFromPP = ppInstance.recv(2048)

    recvInfo = give_list(recvMsgFromPP)

    print("Received message...")
    print(recvInfo)

    cardNumber = recvInfo[0]
    print(cardNumber)
    print(CIF_number[str(cardNumber)])

    # ppInstance.send("1".encode())



