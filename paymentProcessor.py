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
	"GANESH":['GANESH','1001 0110 2002 0026','2023-07-31','002','GANESH T S']
}
# function for converting the binary message into list
# Input is receved message from payment gateway
# output is full message in list
def give_list(recvMessage):
	recvMessage = recvMessage.decode()
	
	recvMessage2 = eval(recvMessage)
	
	return recvMessage2



payProPortNumber = 9999

payProInstance = socket(AF_INET, SOCK_STREAM)
payProInstance.bind(('',payProPortNumber))
payProInstance.listen(1)

print("Payment processor is listening...")
while 1:
	
	paygateInstance, paygetAddress = payProInstance.accept()
	
	print("Connection excepted...:)")
	
	recvMessage = paygateInstance.recv(4096)
	print("Something RECEIVED...:)")
	
	paygateInstance.send("Ture".encode())
	
	# Generate the otp Number
	Otp_Generation = randint(100001, 999999)
	print("This user OTP (ONE TIME PASSWORD) is: ", Otp_Generation)
	
	# Receive the payment amount
	recvAmount = paygateInstance.recv(4096)
	
	
	recvMsg = give_list(recvMessage)
	recvAmt = give_list(recvAmount)
	
	print(recvMsg)
	print("Amount requested :", recvAmt)
	
	paygateInstance.close()
	
	otpinstance, otpaddress = payProInstance.accept()
	
	print("Ready to listen OTP...")
	
	recvOTP = otpinstance.recv(2048)
	recvotp = recvOTP.decode()
	print(type(str(Otp_Generation)))
	print(type(recvotp))
	
	print(int(recvotp)+Otp_Generation)
	
	print("Received OTP from user : ", recvotp)
	if (recvotp == str(Otp_Generation)):
		print("1")
		conf =1
		otpinstance.send("True".encode())
	else:
		conf =0
		otpinstance.send(str(conf).encode())
	
	
	otpinstance.close()

    
   


