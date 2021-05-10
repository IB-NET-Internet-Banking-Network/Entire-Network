"""
Vishnu... thank you for electronics
Author :- Ganesh T S, Manas Kumar mishra

Task :- Design for Transaction processing system (TPS). That perform the OTP part.

Begin DATE :- 05- MARCH- 2021

"""


from socket import *
import datetime
from random import randint
import pymysql
from AES_encrypt import*  #Python file name for encryption
from AES_Decrypt import*  #Python file name for decryption


conn = pymysql.connect( host='localhost', user='root',  password = "", db='test',)


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


# Funtion for debiting and crediting

# Inputs are payee and payer account numbers and amount

# No outputs

def debcred(account1,account2,amount):

        amount1=round(1.01*amount,2)

        a=datetime.datetime.now()

        serverName = '169.254.142.108'

        serverPort = 9048

        clientSocket = socket(AF_INET, SOCK_STREAM)

        # Debit operation

        sentence = account1 + ' debit ' + str(amount1)+' ' + account2

        clientSocket.connect((serverName,serverPort))

        shkey=clientSocket.recv(2048)	
        encrypteddata=str(AES_encrypt(shkey,sentence))
        clientSocket.send(encrypteddata.encode())

        shky=share_key()
        clientSocket.send(shky.encode())
        edata = clientSocket.recv(4096)
        edata = edata.decode()
        edata = eval(edata)
        edata = AES_Decrypt(edata[0],edata[1])
        print(edata)
        b=datetime.datetime.now()
        print(" Elapsed time : ")

        print(b-a)

        clientSocket.close()
        if edata=="Transaction over Successfully":

            # client side

            serverPort = 12000

            clientSocket = socket(AF_INET, SOCK_STREAM)


            # Credit operation

            sentence = account2 + ' credit ' + str(amount)+' ' + account1

            clientSocket.connect((serverName,serverPort))

            shkey=clientSocket.recv(2048)	
            encrypteddata=str(AES_encrypt(shkey,sentence))
            clientSocket.send(encrypteddata.encode())

            shky=share_key()
            clientSocket.send(shky.encode())
            edata1 = clientSocket.recv(4096)
            edata1 = edata1.decode()
            edata1 = eval(edata1)
            edata1 = AES_Decrypt(edata1[0],edata1[1])
            print(edata1)
            b=datetime.datetime.now()
            print(" Elapsed time : ")
            print(b-a)
            clientSocket.close()
            if edata1=="Transaction over Successfully":
                clientSocket2 = socket(AF_INET, SOCK_STREAM)
                #Payment charges
                sentence = '90000000000011' + ' credit ' + str(amount1-amount)+' ' + account1
                clientSocket2.connect((serverName,serverPort))
                shkey=clientSocket2.recv(2048)	
                encrypteddata=str(AES_encrypt(shkey,sentence))
                clientSocket2.send(encrypteddata.encode())

                shky=share_key()
                clientSocket2.send(shky.encode())
                edata2 = clientSocket2.recv(4096)
                edata2 = edata2.decode()
                edata2 = eval(edata2)
                edata2 = AES_Decrypt(edata2[0],edata2[1])
                print(edata2)
                b=datetime.datetime.now()

                print(" Elapsed time : ")

                print(b-a)

                clientSocket2.close()
                if edata2=="Transaction over Successfully":
                    return 0
                else:
                    return 1
            else:
                return 1
        else:
            return 1





TpsServer = socket(AF_INET, SOCK_STREAM)


TpsServer.bind(('', 9988))
TpsServer.listen(1)


print("TPS is ready to connected with pp ...")



a=datetime.datetime.now()


try:
    ppInstance, ppAddress = TpsServer.accept()
    print("Connection accepted with pp...")
except:
    print("Connection not accepted!!!")




while 1:


    # Receiving the list 

    shky=share_key()
    ppInstance.send(shky.encode())
    recvMsgFromPP = ppInstance.recv(2048)
    #recvInfo = give_list(recvMsgFromPP)

    recvMsgFromPP=recvMsgFromPP.decode()
    recvMsgFromPP=eval(recvMsgFromPP)	
    recvMsgFromPP = AES_Decrypt(recvMsgFromPP[0],recvMsgFromPP[1])	
    recvInfo=recvMsgFromPP.split(",")
    print('decrypt',recvInfo)


    print("Received message")
    print(recvInfo)


    cardNumber = recvInfo[0]

        #From card number pick account number

    cur = conn.cursor()

    cur.execute("select AccountNumber from cardaccount where CardNumber = %s",cardNumber)

    AccountNumber= str(cur.fetchall()).replace('(','').replace(')','').replace(',','')    
    
    amount=float(recvInfo[2])
    

    merchantName = recvInfo[3]

    print("Merchant Name : ", merchantName)
    


    cur.execute("select AccountNumber from bank2 where Name = %s",merchantName)

    AccountNumber2= str(cur.fetchall()).replace('(','').replace(')','').replace(',','')
    

    OTP = otp_gen()


    shky=share_key()
    ppInstance.send(shky.encode())

    receivedOtp=ppInstance.recv(2048)
    #recvotp = receivedOtp.decode()
    receivedOtp=receivedOtp.decode()
    receivedOtp=eval(receivedOtp)	
    recvotp = AES_Decrypt(receivedOtp[0],receivedOtp[1])

    print("RECEIVED OTP from the user :- ",recvotp)


    if recvotp == str(OTP):
        zero=1
        zero = debcred(AccountNumber,AccountNumber2,amount)
        if zero == 0:
            sharekey=ppInstance.recv(2048)
            print('shke',sharekey)
            Plaintext='True'
            encrypteddata=str(AES_encrypt(sharekey,Plaintext))
            ppInstance.send(encrypteddata.encode())
            print('feedback sent')
        else:
            sharekey=ppInstance.recv(2048)
            Plaintext='False1'
            encrypteddata=str(AES_encrypt(sharekey,Plaintext))
            ppInstance.send(encrypteddata.encode())



    else:

        sharekey=ppInstance.recv(2048)
        Plaintext='False2'
        encrypteddata=str(AES_encrypt(sharekey,Plaintext))
        ppInstance.send(encrypteddata.encode())


    # ppInstance.close()

    # ppInstance.send("1".encode())
 

