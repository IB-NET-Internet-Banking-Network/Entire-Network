"""

Author :- Manas Kumar mishra
Task :- Design a web app for payment gateway process
Begin DATE :- 05- MARCH- 2021
"""
from flask import Flask, render_template, url_for, request, redirect
from random import randint
from socket import*
from datetime import datetime
from AES_Encrypt import*  #Python file name for encryption
from AES_Decrypt import*  #Python file name for decryption


# Estiblish the connection to the payment processor
payProPortNumber = 9999         #payment processor port number
payproAddress = '169.254.142.108' #payment processor IP address
 #Define the instance of the socket

# print("Not able to connect the payment processor!!!")

"""
Function for sending the data to the payment processor.
Input is details of the users and payment Amount with transaction time
Output is the confirmation about the user and otp page display eligibility
"""
def sendData(fullData, paymentAmount):

    
    payProPortNumber = 9999       #payment processor port number
    payproAddress = '169.254.142.108' #payment processor IP address

    paygateSocket = socket(AF_INET, SOCK_STREAM) #Define the instance of the socket

    try:
        # connect to the payment processor
        paygateSocket.connect((payproAddress, payProPortNumber))
        print("Server is connected...")
    except:
        print("Not able to connect the payment processor!!!")

    fulldata = str(fullData)

    # Todo:- encryption


     # encryption of user data
    Plaintext=str(fullData[0])
    for i in range(1,len(fullData)):
        Plaintext=Plaintext+','+fullData[i]
    print('plaintext: ',Plaintext)

    shkey=paygateSocket.recv(2048)
    encrypteddata=str(AES_encrypt(shkey,Plaintext))
    paygateSocket.send(encrypteddata.encode())
    #paygateSocket.send(fulldata.encode())
    print("User information sent to the payment processor, and waiting for confirmation...")
   
    # confirmation
    
    # Todo :- Decryption

    Confirmmes=share_key()
    paygateSocket.send(Confirmmes.encode())

    confirmation = paygateSocket.recv(2048)
    conf=confirmation.decode()
    conf=eval(conf)
    mes=AES_Decrypt(conf[0],conf[1])
    print('feedback: ',mes)

    #confirmation = paygateSocket.recv(2048)
    # print("Response received...")
    # print(confirmation.decode())
    
    if mes=="True":
        Plaintext=str(paymentAmount[0])
        for i in range(1,len(paymentAmount)):
            Plaintext=Plaintext+','+paymentAmount[i]
        print('plaintext: ',Plaintext)
        shkey=paygateSocket.recv(2048)        
        encrypteddata = str(AES_encrypt(shkey,Plaintext))
        paygateSocket.send(encrypteddata.encode())
        
        print(" Amount Data sent... :- )")
    else:
        print("Amount data stop here, confirmation error!!!")
    paygateSocket.close()

    return mes


def send_otp(UserOTP):
    payProPortNumber = 9999       #payment processor port number
    payproAddress = '169.254.142.108' #payment processor IP address

    otpsocket = socket(AF_INET, SOCK_STREAM)

    try:
        otpsocket.connect((payproAddress, payProPortNumber))
        print("Payment processor is connected...")
    except:
        print("Not able to connect the payment processor!!!")
    
    #otp encryption
    
    userotp = str(UserOTP)
    sharekey=otpsocket.recv(2048)
    encrypteddata=AES_encrypt(sharekey,userotp)
    otpsocket.send(str(encrypteddata).encode()) 
    #otpsocket.send(userotp.encode())
    print("otp sent")

    #send public key for encryption
    Confirmmes=share_key()
    otpsocket.send(Confirmmes.encode())

    #decrypting feedback from TPS
    CHeck=otpsocket.recv(1024)
    check = CHeck.decode()
    
    conf=eval(check)
    check=AES_Decrypt(conf[0],conf[1])
    otpsocket.close()
    return check



# The formal list for registered users
# It is a global variable that can be assesible from anypart of the code

global ListOfUsers
ListOfUsers = {
    "MANAS":"ESD18I011",
    "MISS KR":"EDM18B026",
    "GANESH":"ESD18I006"
}

# global numberOfAtm
# numberOfAtm =0

global merchantList
merchantList = {
    "0":"Income Tax Authority",
    "1":"Amazon",
    "2":"Zomato",
    "3":"Internshala",
    "4":"MakeMyTrip",
    "5":"Practo",
    "6":"MKMISHRA",
    "7":"OlaCabs",
    "8":"UberCabs",
    "9":"IRCTC"
}


"""
Function for authentication of the users
Input is username and password from the payment gateway page 
Output is True if user is correct else False
""" 
def userAuthentication(username, password):
    print("This user rgistered password is :", ListOfUsers[username])
    if (ListOfUsers[username] == password):
        print("Correct password")
        return True
    else:
        return False


"""
Fuunction for printing the data on the backend screen
input is the details of the user entered on the page
Output is nothing but in between it is printing the information
"""
def backEndInfo(loginusesr, UsercardNumber, ExpiryDate, CVVNumber, CardHolderName, AmountForPaying, merchant, cardInfo):

    now = datetime.now()
    print("Login user        : ", loginusesr)
    print("Card number       : ", UsercardNumber)
    print("Expiry Date       : ", ExpiryDate)
    print("CVV number        : ", CVVNumber)
    print("Card Holder name  : ", CardHolderName)
    print("Amount requested  : ", AmountForPaying)
    print("Paying to         : ", merchant)
    print("Time of payment   : ", now)
    if cardInfo ==1:
        print("Method of payment :  Debit card")
    elif cardInfo == 0:
        print("Method of payment :  Credit card")
    else:
        print("No card details !!!!!!!!!!!!!!!!!")

    PutData = open("Payment_Gateway_record.txt", "a")
    messageinput0 = ("-------------------------------------------------------"+"\n")
    messageinput1 = ("**Login user           : "+ loginusesr+"\n")
    messageinput2 = ("**Card number          : "+ UsercardNumber+"\n")
    messageinput3 = ("**Expiry Date          : "+ ExpiryDate+"\n")
    messageinput4 = ("**CVV number           : "+ CVVNumber+"\n")
    messageinput5 = ("**Card holder name     : "+ CardHolderName+"\n")
    messageinput6 = ("**Amount Requested     : "+ AmountForPaying+"\n")
    messageinput7 = ("**Paying to            : "+ merchant+"\n")
    messageinput8 = ("**Time of transaction  : "+ str(now)+"\n")
    messageinput9 = ("---------------------------------------------------------"+"\n")
    PutData.write(messageinput0)
    PutData.write(messageinput1)
    PutData.write(messageinput2)
    PutData.write(messageinput3)
    PutData.write(messageinput4)
    PutData.write(messageinput5)
    PutData.write(messageinput6)
    PutData.write(messageinput7)
    PutData.write(messageinput8)
    PutData.write(messageinput9)
    PutData.close()


# Flask operations
app = Flask(__name__)

# Secret key for security
app.config['SECRET_KEY'] = '81385de1a511d795a323d3866f4fc7c1'

# decorators @ for app routing
@app.route('/payments', methods = ["POST", "GET"])
def hello():

    megOnPage = ""  # Message for users

    # Check the request first 
    # GET for putting content on webapp
    # POST for receive the content from webapp
    if request.method == "POST":

        # Store the user name, Password and Method of payment
        user = request.form["name"]
        password = request.form["pass"]
        methodOfPayment = request.form["Method"]

        # Check user filled the details
        if (str(user) == "" or str(password)==""):
            megOnPage = "Please fill the login details !!!"
            return (render_template('loginPage.html', message = megOnPage))

        
        # print the username and password
        print("Username " + str(user))
        print("Password "+ str(password))
        print("Method of payment =" + str(methodOfPayment))


        if (userAuthentication(str(user), str(password))):
            if (str(methodOfPayment) == "Debit card"):
                return redirect(url_for("DebitCardPayment", usr=user))

            if (str(methodOfPayment) == "Credit card"):
                return redirect(url_for("CreditCardPayment", usr=user))

            else:
                return (redirect(url_for("ErrorInMethodOfPayment", usr=user)))

        else:
            return (render_template('loginPage.html'))
       
    else:
        # For get method we will stay on the same page
        return (render_template('loginPage.html'))

merchant = ''
@app.route("/Debitcard/<usr>", methods = ["POST", "GET"])
def DebitCardPayment(usr):
    message = "" # user information
    global merchant

    if request.method == "POST":

        # User card information
        UsercardNumber = request.form["cardNumber"]
        ExpiryDate = request.form["expiryDate"]
        CVVnumber = request.form["CVVNumber"]
        AmountForPaying = request.form["AmountPay"]
        CardHolderName = request.form["CardHolderName"]

        # Check the data are filled by user or not
        if(str(UsercardNumber)==""or str(ExpiryDate)=="" or str(CVVnumber)=="" or str(AmountForPaying)=="" or str(CardHolderName)==""):
            print("No details")
            message = "Please fill, proper full  details !!!"
            return render_template('card1.html', post=str(usr), nxt=str(merchant),message=message)
        else:
            backEndInfo(str(usr), str(UsercardNumber), str(ExpiryDate), str(CVVnumber), str(CardHolderName), str(AmountForPaying), str(merchant), 1)

            fullData = [str(usr), str(UsercardNumber), str(ExpiryDate), str(CVVnumber), str(CardHolderName)]

            now = datetime.now()
            payingAmount = [str(AmountForPaying),str(merchant), str(now)]

            confirmation = sendData(fullData, payingAmount)
            print("Received confirmation about user from payment Processor :", confirmation)
            
            if confirmation=="True":
                return redirect(url_for("paid"))
            else:
                return f"""<h1>ERROR, Wrong data input</h1>"""
    else:
        merchantID = randint(0,9)
        merchant = merchantList[str(merchantID)]

        return render_template('card1.html', post=str(usr), nxt=str(merchant),message=message)


merchant = ''
@app.route("/Creditcard/<usr>", methods = ["POST", "GET"])
def CreditCardPayment(usr):
    message = "" # User Information
    global merchant
    merchantID = randint(0,9)
    merchant = merchantList[str(merchantID)]
    print("Login user :",str(usr))

    if request.method == "POST":

        # User card information
        UsercardNumber = request.form["cardNumber"]
        ExpiryDate = request.form["expiryDate"]
        CVVnumber = request.form["CVVNumber"]
        AmountForPaying = request.form["AmountPay"]
        CardHolderName = request.form["CardHolderName"]

        # Check the data are filled by user or not 
        if(str(UsercardNumber)==""or str(ExpiryDate)=="" or str(CVVnumber)=="" or str(AmountForPaying)=="" or str(CardHolderName)==""):
            print("No details")
            message = "Please fill, proper full  details !!!" # Display message to the user
            return render_template('card1.html', post=str(usr), nxt=str(merchant),message=message)
        else:
            backEndInfo(str(usr), str(UsercardNumber), str(ExpiryDate), str(CVVnumber), str(CardHolderName), str(AmountForPaying),str(merchant), 0)
            
            fullData = [str(usr), str(UsercardNumber), str(ExpiryDate), str(CVVnumber), str(CardHolderName)]
            now = datetime.now()
            payingAmount = [str(AmountForPaying), str(merchant), str(now)]

            confirmation = sendData(fullData, payingAmount)

            print("Received confirmation about user from payment Processor :", confirmation)

            if confirmation=="True":
                return redirect(url_for("paid"))
            else:
                return f"""<h1>ERROR, Wrong data input</h1>"""
            
    else:

        merchantID = randint(0,9)
        merchant = merchantList[str(merchantID)]
        
        return render_template('card1.html', post=str(usr), nxt=str(merchant),message=message)


@app.route("/Error/<usr>", methods = ["POST", "GET"])
def ErrorInMethodOfPayment(usr):
    return f"""<h1>ERROR , method of Payment is not given</h1>"""


@app.route("/otpPage/", methods=["POST", "GET"])
def paid():
    
    print("OTP page display")
    
    if request.method == "POST":

        OTPnumber = request.form["OTP"]
        print("OTP filled by user : ", str(OTPnumber))

        check = send_otp(OTPnumber)
        print(check)
        if check == "True":
            print("Correct OTP, your are paying...")
            return (render_template('finalResult.html'))
        elif check == "False1":
            print("Correct OTP, but insufficient balance")
            return (render_template('finalResult2.html'))
        else:
            print("Wrong OTP, payment failed !!!")
            return f"""<h1>WRONG OTP... payment failed !!! :( </h1>"""
       
    else:
        return render_template('otp.html')



if __name__ == "__main__":
    app.run(port= 1000, debug=True)

