import pymysql 
from socket import *
import datetime

a=datetime.datetime.now()
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ("The server is ready to receive")
while 1:
        connectionSocket, addr = serverSocket.accept()
        print("Connection Accepted")
        sentence = connectionSocket.recv(2048)
        print("Sentence Received")
        sentence=sentence.decode().split()
        account=sentence[0]
        tt=sentence[1]
        print(tt)
        amount=float(sentence[2])
        conn = pymysql.connect( host='localhost', user='root',  password = "", db='test',) 
        cur = conn.cursor()
        cur.execute("select balance from bank2 where AccountNumber = %s",account) 
        balance = str(cur.fetchall()).replace('(','').replace(')','').replace(',','')
        balance=float(balance)
        if(tt=='debit'):
            if(balance>amount):
                    balance=balance - amount
                    print(balance)
            else:
                    print(" Low Balance")
        elif(tt=='credit'):
            balance=balance + amount
            print(balance)
        else:
            print("illegal operation")
        update="update bank2 set balance = "+str(balance)+" where AccountNumber = "+account
        cur.execute(update)
        update="update bank2 set lastt = now() where AccountNumber = "+account
        cur.execute(update)
        conn.commit()
        conn.close()
        connectionSocket.send("Transaction over".encode())
        b=datetime.datetime.now();
        print(" Elapsed time : ")
        print(b-a)
        connectionSocket.close()

  

