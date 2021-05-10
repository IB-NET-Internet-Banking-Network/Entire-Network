import pymysql 
from socket import *
import datetime
from AES_encrypt import*  #Python file name for encryption
from AES_Decrypt import*  #Python file name for decryption

#function for unsuccessful cases
def unsuccessful():
    conn.commit()
    conn.close()
    sharekey=connectionSocket.recv(2048)        
    Plaintext="Transaction Unsuccessfull"
    encrypteddata=str(AES_encrypt(sharekey,Plaintext))
    connectionSocket.send(encrypteddata.encode())
    b=datetime.datetime.now()
    print(" Elapsed time : ")
    print(b-a)
    connectionSocket.close()

a=datetime.datetime.now()
serverPort = 9048
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ("The server is ready to receive")
while 1:
        connectionSocket, addr = serverSocket.accept()
        print("Connection Accepted")

        shky=share_key()
        connectionSocket.send(shky.encode())
        sentence=connectionSocket.recv(2048)
        print("Sentence Received")
        sentence=sentence.decode()
        sentence=eval(sentence)	
        sentence = AES_Decrypt(sentence[0],sentence[1])
        sentence=sentence.split()
        print(sentence)

        account=sentence[0]
        tt=sentence[1]
        print("Transaction Type:")
        print(tt)
        amount=float(sentence[2])
        account2=sentence[3]
        conn = pymysql.connect( host='localhost', user='root',  password = "", db='test',) 
        cur = conn.cursor()
        cur.execute("select Balance from bank where AccountNumber = " + account) 
        balance = str(cur.fetchall()).replace('(','').replace(')','').replace(',','')
        balance=float(balance)
        if(tt=='debit'):
            if(balance>amount):
                    balance=balance - amount
                    print("Updated Balance :")
                    print(balance)
            else:
                    print(" Low Balance")
                    unsuccessful()
                    continue
        elif(tt=='credit'):
            balance=balance + amount
            print("Updated Balance :")
            print(balance)
        else:
            print("illegal operation")
            unsuccessful()
            continue
        update="update bank set balance = "+str(balance)+" where AccountNumber = "+account
        cur.execute(update)
        update="update bank set lastt = now() where AccountNumber = "+account
        cur.execute(update)

        sharekey=connectionSocket.recv(2048)        
        Plaintext="Transaction over Successfully"
        encrypteddata=str(AES_encrypt(sharekey,Plaintext))
        connectionSocket.send(encrypteddata.encode())

        b=datetime.datetime.now()
        cur.execute("select CIF from bank where AccountNumber = " + account) 
        CIF = str(cur.fetchall()).replace('(','').replace(')','').replace(',','').replace("'","")
        cur.execute("select Name from bank2 where AccountNumber = " + account2) 
        Party = str(cur.fetchall()).replace('(','').replace(')','').replace(',','')
        name=CIF + ".txt"
        f = open(CIF + ".txt", "a")
        f.write("\n--------------------\n")
        f.write("Account Number: "+account+"\n")
        f.write("Amount : "+str(amount)+"\n")
        f.write("Type of Transaction: "+tt+"\n")
        f.write("Time of Transaction: "+str(datetime.datetime.now())+"\n")
        f.write("Party: "+Party+"("+account2+")"+"\n")
        f.write("--------------------\n")
        f.close()
        conn.commit()
        conn.close()
        
        print(" Elapsed time : ")
        print(b-a)
        connectionSocket.close()

        
  

