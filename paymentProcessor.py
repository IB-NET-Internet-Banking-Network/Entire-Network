"""
Author :- Manas Kumar Mishra
Task :- Payment process (client for card company and server for payment gateway)
Begin date :- 21 - March - 2021 
"""

from socket import*
from random import randint

global dataofUsers
dataofUsers ={
	'MANAS':['MANAS', '1001 0110 2002 0011', '2023-07-31', '000', 'MANAS KUMAR MISHRA'],
	'MISS KR':['MISS KR','1001 0110 2002 0026','2023-07-31','001','KARTHIKA RAJESH'],
	"GANESH":['GANESH','1001 0110 2002 0006','2023-07-31','002','GANESH T S']
}

# function for converting the binary message into list
# Input is receved message from payment gateway
# output is full message in list
def give_list(recvMessage):
	recvMessage = recvMessage.decode()

	recvMessage2 = eval(recvMessage)

	return recvMessage2




payProPortNumber = 9999

TPSportnumber = 9988
TPSipaddress = '192.168.43.99'

payProInstance = socket(AF_INET, SOCK_STREAM)
TPSsocket = socket(AF_INET,SOCK_STREAM)

payProInstance.bind(('',payProPortNumber))
payProInstance.listen(1)


print("Payment processor is listening...")
while 1:
	
	paygateInstance, paygetAddress = payProInstance.accept()
	TPSsocket.connect((TPSipaddress, TPSportnumber))
	print("Connection excepted...:)")
	
	recvMessage = paygateInstance.recv(4096)
	print("Something RECEIVED...:)")

	recvMsg = give_list(recvMessage)
	print(recvMsg)
	
	if(recvMsg==list(dataofUsers['MANAS']) or recvMsg==list(dataofUsers['MISS KR']) or recvMsg == list(dataofUsers['GANESH'])):
		paygateInstance.send("True".encode())

		# Receive the amount details
		recvAmount = paygateInstance.recv(2048)

		recvAmt = give_list(recvAmount)

		paygateInstance.close()

		# Todo:- TPS PART. 
		# Here , we are making a packet for communicating with TPS layer
		packet = []
		# Card number 
		packet.append(recvMsg[1]) 

		# Card holder name 
		packet.append(recvMsg[4])

		# Amount and merchent 
		packet.append(recvAmt[0])
		packet.append(recvAmt[1])
		packet.append(recvAmt[2])

		packet = str(packet)
		TPSsocket.send(packet.encode())

		
		print("Amount requested :", recvAmt[0])

	else:
		paygateInstance.send("False".encode())
		paygateInstance.close()

		print("Wrong detalis")


	otpinstance, otpaddress = payProInstance.accept()
	
	print("Ready to listen OTP...")
	
	recvOTP = otpinstance.recv(2048)
	
	# Todo :- Encryption and decryption
	TPSsocket.send(recvOTP)

	print("Otp send to the TPS")
	recv = TPSsocket.recv(2048)

	print("Received feedback about otp")
	otpinstance.send(recv)

	TPSsocket.close()
	otpinstance.close()

    
   


