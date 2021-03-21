"""
Author :- Manas Kumar mishra
Task :- Design a web app for payment gateway process
Begin DATE :- 05- MARCH- 2021
"""
from flask import Flask, render_template, url_for, request, redirect
from random import randint
from socket import*


# Estiblish the connection to the payment processor
payProPortNumber = 9999       #payment processor port number
payproAddress = '192.168.43.99' #payment processor IP address
 #Define the instance of the socket

# print("Not able to connect the payment processor!!!")

def sendData(fullData, paymentAmount):
    
    payProPortNumber = 9999       #payment processor port number
    payproAddress = '192.168.43.99' #payment processor IP address

    paygateSocket = socket(AF_INET, SOCK_STREAM) #Define the instance of the socket

    try:
        # connect to the payment processor
        paygateSocket.connect((payproAddress, payProPortNumber))
        print("Server is connected...")
    except:
        print("Not able to connect the payment processor!!!")

    fulldata = str(fullData)

    paygateSocket.send(fulldata.encode())

    # confirmation
    confirmation = paygateSocket.recv(2048)
    
    paygateSocket.send(str(paymentAmount).encode())
        
    print("Data sent...:)")
    paygateSocket.close()

    return confirmation.decode()


def send_otp(UserOTP):
    payProPortNumber = 9999       #payment processor port number
    payproAddress = '192.168.43.99' #payment processor IP address

    otpsocket = socket(AF_INET, SOCK_STREAM)

    try:
        otpsocket.connect((payproAddress, payProPortNumber))
        print("Payment processor is connected...")
    except:
        print("Not able to connect the payment processor!!!")
    
    userotp = str(UserOTP)

    otpsocket.send(userotp.encode())
    CHeck=otpsocket.recv(1024)
    check = CHeck.decode()

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

global merchentList
merchentList = {
    "0":"Income tax authority",
    "1":"AMAZON",
    "2":"Zomato",
    "3":"Intershala",
    "4":"Make My Trip",
    "5":"Practo",
    "6":"mkmishra2000",
    "7":"Ola cabs",
    "8":"Uber cabs",
    "9":"IRTC train ticket"
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

        # Store the user name and Password
        user = request.form["name"]
        password = request.form["pass"]
        methodOfPayment = request.form["Method"]

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


@app.route("/Debitcard/<usr>", methods = ["POST", "GET"])
def DebitCardPayment(usr):
    message = "" # user information
    merchentID = randint(0,9)
    merchent = merchentList[str(merchentID)]
    print("Login user :",str(usr))

    if request.method == "POST":

        # User card information
        UsercardNumber = request.form["cardNumber"]
        ExpiryDate = request.form["expiryDate"]
        CVVnumber = request.form["CVVNumber"]
        AmountForPaying = request.form["AmountPay"]
        CardHolderName = request.form["CardHolderName"]

        # Check the data are filled by user or not
        if(str(UsercardNumber)==""or str(ExpiryDate)=="" or str(CVVnumber)=="" or str(AmountForPaying)==""):
            print("No details")
            message = "Please fill, proper full  details !!!"
            return render_template('card1.html', post=str(usr), nxt=str(merchent),message=message)
        else:
            print("Card Number is :", str(UsercardNumber))
            print("Expiry date is :", str(ExpiryDate))
            print("Cvv Number is :", str(CVVnumber))
            print("Card Holder Name :", str(usr))
            print("Amount for paying :", str(AmountForPaying))
            print("Card Holder name :", str(CardHolderName))
            print("method of payment is debit card")

            fullData = [str(usr), str(UsercardNumber), str(ExpiryDate), str(CVVnumber), str(CardHolderName)]
            payingAmount = [str(AmountForPaying)]

           
            confirmation = sendData(fullData, payingAmount)
            print("Recived confirmation about user from payment gatway :", confirmation)
            
            return redirect(url_for("paid"))
    else:
        return render_template('card1.html', post=str(usr), nxt=str(merchent),message=message)


@app.route("/Creditcard/<usr>", methods = ["POST", "GET"])
def CreditCardPayment(usr):
    message = "" # User Information
    merchentID = randint(0,9)
    merchent = merchentList[str(merchentID)]
    print("Login user :",str(usr))

    if request.method == "POST":

        # User card information
        UsercardNumber = request.form["cardNumber"]
        ExpiryDate = request.form["expiryDate"]
        CVVnumber = request.form["CVVNumber"]
        AmountForPaying = request.form["AmountPay"]
        CardHolderName = request.form["CardHolderName"]

        # Check the data are filled by user or not 
        if(str(UsercardNumber)==""or str(ExpiryDate)=="" or str(CVVnumber)=="" or str(AmountForPaying)==""):
            print("No details")
            message = "Please fill, proper full  details !!!" # Display message to the user
            return render_template('card1.html', post=str(usr), nxt=str(merchent),message=message)
        else:
            print("Card Number is :", str(UsercardNumber))
            print("Expiry date is :", str(ExpiryDate))
            print("Cvv Number is :", str(CVVnumber))
            print("Card Holder Name :", str(usr))
            print("Amount for paying :", str(AmountForPaying))
            print("Card Holder name :", str(CardHolderName))
            print("method of payment is debit card")
            
            return redirect(url_for("paid"))
    else:
        return render_template('card1.html', post=str(usr), nxt=str(merchent),message=message)


@app.route("/Error/<usr>", methods = ["POST", "GET"])
def ErrorInMethodOfPayment(usr):
    return f"""<h1>ERROR , method of Payment is not given</h1>"""


@app.route("/otpPage/", methods=["POST", "GET"])
def paid():
    
    print("OTP page display")
    
    if request.method == "POST":

        OTPnumber = request.form["OTP"]
        print("OTP is : ", str(OTPnumber))

        check = send_otp(OTPnumber)
        print(check)
        if check == "True":
            return f"""<h1>Payment is in progress...wait for a while : )</h1>"""
        else:
            return f"""<h1>WRONG OTP... payment failed !!! :( </h1>"""
        return f"""<h1>Payment is in progress...wait for a while</h1>"""
    else:
        return render_template('otp.html')

  
if __name__ == "__main__":
    app.run(port= 1000, debug=True)

