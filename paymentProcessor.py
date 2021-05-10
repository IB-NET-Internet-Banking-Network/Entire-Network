"""
Author :- Manas Kumar Mishra
Task :- Payment process (client for card company and server for payment gateway)
Begin date :- 21-March-2021 
"""

from socket import*
from random import randint
from AES_Encrypt import*  #Python file name for encryption
from AES_Decrypt import*  #Python file name for decryption

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
TPSipaddress = '169.254.142.108'

payProInstance = socket(AF_INET, SOCK_STREAM)
TPSsocket = socket(AF_INET,SOCK_STREAM)
try:
	TPSsocket.connect((TPSipaddress, TPSportnumber))
	print("Connection accepted with TPS...:)")
except:
	print("Connection not accepted with TPS!!!")



# TPSsocket.connect((TPSipaddress, TPSportnumber))


payProInstance.bind(('',payProPortNumber))
payProInstance.listen(1)


print("Payment processor is listening...")
while 1:
	
	paygateInstance, paygetAddress = payProInstance.accept()
	
	print("Connection accepted...:)")
	
	# recieving user data 

	Shared=share_key() #sharing public key for encryption
	paygateInstance.send(Shared.encode())
	
	#Decryption
	recvMessage = paygateInstance.recv(4096)
	print("Something RECEIVED...:)",recvMessage)
	#recvMsg = give_list(recvMessage)
	recvmsg=recvMessage.decode()
	recvMsg=eval(recvmsg)	
	recvMsg = AES_Decrypt(recvMsg[0],recvMsg[1])	
	recvMsg=recvMsg.split(",")
	print('decrypted message',recvMsg)
	
	if(recvMsg==list(dataofUsers['MANAS']) or recvMsg==list(dataofUsers['MISS KR']) or recvMsg == list(dataofUsers['GANESH'])):
		#send feedback after data verification
		sharekey=paygateInstance.recv(2048)
		Plaintext='True'
		encrypteddata=str(AES_encrypt(sharekey,Plaintext))
		paygateInstance.send(encrypteddata.encode())

		# Receiving the amount details 
		print("Receiveing the amount info....")
		shky=share_key()
		paygateInstance.send(shky.encode())
		recvAmount = paygateInstance.recv(2048)
		recvAmt = recvAmount.decode()
		recvAmt = eval(recvAmt)
		recvAmt = AES_Decrypt(recvAmt[0],recvAmt[1])
		recvAmt=recvAmt.split(",")

		print("Amount received...")
		
		print("Amount requested :", recvAmt)

		paygateInstance.close()

		# TPS PART. 
		# Here , we are making a packet for communicating with TPS layer
		packet = []
		# Card number 
		packet.append(recvMsg[1]) 

		# Card holder name 
		packet.append(recvMsg[4])

		# Amount and merchant 
		packet.append(recvAmt[0])
		packet.append(recvAmt[1])
		packet.append(recvAmt[2])

			

		# TPSsocket.connect((TPSipaddress, TPSportnumber))
		try:
			Plaintext=str(packet[0])
			for i in range(1,len(packet)):
				Plaintext=Plaintext +','+ packet[i]
		
			shkey=TPSsocket.recv(2048)
			encrypteddata=str(AES_encrypt(shkey,Plaintext))
			TPSsocket.send(encrypteddata.encode())
			print('packet',packet)
			print('packet',Plaintext)
			print("Message (packet) sent to TPS")
		except:
			print("Not sending data to TPS")

		
		print("Amount requested :", recvAmt[0])

	else:
		shkey=TPSsocket.recv(2048)
		Plaintext='False'
		encrypteddata=str(AES_encrypt(shkey,Plaintext))
		TPSsocket.send(encrypteddata.encode())
		paygateInstance.close()

		print("Wrong detalis")


	
	#PP CONNECTED TO APP
	otpinstance, otpaddress = payProInstance.accept()
	
	print("Ready to listen OTP...")
	
	shky=share_key()
	otpinstance.send(shky.encode())
	recvotp = otpinstance.recv(4096)
	recvotp = recvotp.decode()
	recvotp = eval(recvotp)
	recvOTP = AES_Decrypt(recvotp[0],recvotp[1])
	print('otp recieved')
	#recvOTP = otpinstance.recv(2048)
	
	# Todo :- Encryption and decryption
	shkey=TPSsocket.recv(2048)	
	encrypteddata=str(AES_encrypt(shkey,recvOTP))
	TPSsocket.send(encrypteddata.encode())

	print("OTP send to the TPS")

	shky=share_key()	
	TPSsocket.send(shky.encode())
	recve = TPSsocket.recv(2048)
	recve = recve.decode()
	recve = eval(recve)	
	recve = AES_Decrypt(recve[0],recve[1])

	print(recve)
	
	print("Received feedback about OTP")
	shkey=otpinstance.recv(2048)	
	encrypteddata=str(AES_encrypt(shkey,recve))
	otpinstance.send(encrypteddata.encode())

	# TPSsocket.close()
	otpinstance.close()

    
   


