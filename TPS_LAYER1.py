from socket import *
import datetime

a=datetime.datetime.now()

amount=1000

serverName = '169.254.142.108'
serverPort = 9048
clientSocket = socket(AF_INET, SOCK_STREAM)

amount1=amount*1.1

# Todo:- Otp

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

