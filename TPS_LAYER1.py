"""

Author :- Ganesh T S, Manas Kumar mishra

Task :- Design for Transaction processing system (TPS). That perform the OTP part.

Begin DATE :- 05- MARCH- 2021

"""


from socket import *
import datetime

from random import randint

import pymysql

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

        amount1=1.1*amount

        a=datetime.datetime.now()

        serverName = '169.254.142.108'

        serverPort = 9048

        clientSocket = socket(AF_INET, SOCK_STREAM)

        # Debit operation

        sentence = account1 + ' debit ' + str(amount1)+' ' + account2

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

        sentence = account2 + ' credit ' + str(amount)+' ' + account1

        clientSocket.connect((serverName,serverPort))

        clientSocket.send(sentence.encode())

        clientSocket.recv(2048)

        b=datetime.datetime.now()

        print(" Elapsed time : ")

        print(b-a)

        clientSocket.close()
        

        clientSocket2 = socket(AF_INET, SOCK_STREAM)

#Payment charges
        

        sentence = '90000000000011' + ' credit ' + str(amount1-amount)+' ' + account1

        clientSocket2.connect((serverName,serverPort))

        clientSocket2.send(sentence.encode())

        clientSocket2.recv(2048)

        b=datetime.datetime.now()

        print(" Elapsed time : ")

        print(b-a)

        clientSocket2.close()

        return 0





TpsServer = socket(AF_INET, SOCK_STREAM)


TpsServer.bind(('', 9988))
TpsServer.listen(1)


print("TPS is ready to connected with pp ...")



a=datetime.datetime.now()


"""

NOTE:- for ganesh, Amount is coming in the while loop , 3rd element of the recvInfo list is the amount.

Hence if you can add all your socket connection and processes into this while loop then we won't face any issue.

"""




while 1:

    print("start")
    try:
        ppInstance, ppAddress = TpsServer.accept()
        print("Entered Try")
    except:
        print("problem in connection with pp")

    print("Connection established...")


    # todo:- Receiving the list 

    recvMsgFromPP = ppInstance.recv(2048)


    recvInfo = give_list(recvMsgFromPP)


    print("Received message...")

    print(recvInfo)


    cardNumber = recvInfo[0]

    print(cardNumber)

        #From card number pick account number

    cur = conn.cursor()

    cur.execute("select AccountNumber from cardaccount where CardNumber = %s",cardNumber)

    AccountNumber= str(cur.fetchall()).replace('(','').replace(')','').replace(',','')
    

    amount=float(recvInfo[2])
    

    merchantName = recvInfo[3]

    print("Merchant Name : ", merchantName)
    

    # Todo :- From merchant name pick account number

    cur.execute("select AccountNumber from bank2 where Name = %s",merchantName)

    AccountNumber2= str(cur.fetchall()).replace('(','').replace(')','').replace(',','')

    print(AccountNumber2)

    OTP = otp_gen()


    receivedOtp=ppInstance.recv(2048)
    

    recvotp = receivedOtp.decode()


    print("RECEIVED OTP from the user :- ",recvotp)


    if recvotp == str(OTP):

        ppInstance.send("True".encode())

        zero = debcred(AccountNumber,AccountNumber2,amount)

        if zero ==0:
            print("Function completed")

        # Todo:- Banking part.

    else:

        ppInstance.send("False".encode())


    ppInstance.close()
    print('Full while loop completed')

    # ppInstance.send("1".encode())



# Todo:- ADD all below work inside the while loop such that it can communicate properly with bank1, and bank2. 

