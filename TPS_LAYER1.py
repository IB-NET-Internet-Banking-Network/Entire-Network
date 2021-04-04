"""
Author :- Ganesh T S, Manas Kumar mishra
Task :- Design for Transaction processing system (TPS). That perform the OTP part.
Begin DATE :- 05- MARCH- 2021
"""

from socket import *
import datetime
from random import randint


# CIF Customer Information file
# It maaps between the Card info to the Bank information
global CIF_number
CIF_number={
    "1001 0110 2002 0011":"98765432011",
    "1001 0110 2002 0026":"98765432026",
    "1001 0110 2002 0006":"98765432006"
}

# Mapping between the CIF number to the Account detalis
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

# Funtion for generating the Otp
# Input is nothing
# Output is Generated Otp

def otp_gen():
    otpgenerated = randint(100001, 999999)

    print("Generated OTP is :- ", otpgenerated)

    return otpgenerated


TpsPortNumber = 9988

TpsServer = socket(AF_INET, SOCK_STREAM)

TpsServer.bind(('', TpsPortNumber))
TpsServer.listen(1)

serverName = '169.254.142.108'
serverPort = 9048
clientSocket = socket(AF_INET, SOCK_STREAM)

print("TPS is ready to connected with pp ...")


a=datetime.datetime.now()

"""
NOTE:- for ganesh, Amount is coming in the while loop , 3rd element of the recvInfo list is the amount.
Hence if you can add all your socket connection and processes into this while loop then we won't face any issue.
"""
amount=1000
amount1=amount*1.1


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

    OTP = otp_gen()

    receivedOtp=ppInstance.recv(2048)

    recvotp = receivedOtp.decode()

    print("RECEIVED OTP from the user :- ",recvotp)

    if recvotp == str(OTP):
        ppInstance.send("True".encode())
    else:
        ppInstance.send("False".encode())

    ppInstance.close()
    # ppInstance.send("1".encode())


# Todo:- ADD all below work inside the while loop such that it can communicate properly with bank1, and bank2. 

# Debit operation
sentence = '81309831 debit '+str(amount1)

clientSocket.connect((serverName,serverPort))
clientSocket.send(sentence.encode())

b=datetime.datetime.now()

clientSocket.recv(2048)
print(" Elapsed time : ")

print(b-a)

clientSocket.close()

# client side
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

# Credit operation
sentence = '81309832 credit '+str(amount)

clientSocket.connect((serverName,serverPort))
clientSocket.send(sentence.encode())
clientSocket.recv(2048)

b=datetime.datetime.now()
print(" Elapsed time : ")
print(b-a)

clientSocket.close()

