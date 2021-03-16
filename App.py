"""
Author :- Manas Kumar mishra
Task :- Design a web app for payment gateway process
Begin DATE :- 05- MARCH-2021
"""
from flask import Flask, render_template, url_for, request, redirect
from random import randint
# The formal list for registered users
# It is a global variable that can be assesible from anypart of the code

global ListOfUsers
ListOfUsers = {
    "MANAS":"ESD18I011",
    "MISS KR":"EDM18B026",
    "GANESH":"ESD18I006"
}

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

def userAuthentication(username, password):
    print("This user rgistered password is :", ListOfUsers[username])
    if (ListOfUsers[username] == password):
        print("Correct password")
        return True


app = Flask(__name__)

# Secret key for security
app.config['SECRET_KEY'] = '81385de1a511d795a323d3866f4fc7c1'

# decorators @ for app routing
@app.route('/payment', methods = ["POST", "GET"])
def hello():
    # Check the request first 
    # GET for putting content on webapp
    # POST for receive the content from webapp
    if request.method == "POST":

        # Store the user name and Password
        user = request.form["name"]
        password = request.form["pass"]
        methodOfPayment = request.form["Method"]

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
        # Take step based on the input in the form 
        # return render_template("form1.html")
        

        # for new page we can try
        # return redirect(url_for("user", usr= user))
    else:
        # For get method we will stay on the same page
        return (render_template('loginPage.html'))


@app.route("/DebitcardPAY/<usr>", methods = ["POST", "GET"])
def DebitCardPayment(usr):
    
    merchentID = randint(0,9)
    merchent = merchentList[str(merchentID)]
    print(str(usr))

    if request.method == "POST":

        # User card information
        UsercardNumber = request.form["cardNumber"]
        ExpiryDate = request.form["expiryDate"]
        CVVnumber = request.form["CVVNumber"]
        AmountForPaying = request.form["AmountPay"]


        # printing the card information from the page
        print("Card Number is :", str(UsercardNumber))
        print("Expiry date is :", str(ExpiryDate))
        print("Cvv Number is :", str(CVVnumber))
        print("Card Holder Name :", str(usr))
        print("Amount for paying :", str(AmountForPaying))
        print("Method of payment is debit card")

        return redirect(url_for("paid"))
    else:
        return render_template('card1.html', post=str(usr), nxt=str(merchent))


@app.route("/CreditcardPAY/<usr>", methods = ["POST", "GET"])
def CreditCardPayment(usr):

    merchentID = randint(0,9)
    merchent = merchentList[str(merchentID)]
    print(str(usr))

    if request.method == "POST":

        # User card information
        UsercardNumber = request.form["cardNumber"]
        ExpiryDate = request.form["expiryDate"]
        CVVnumber = request.form["CVVNumber"]
        AmountForPaying = request.form["AmountPay"]


        # printing the card information from the page
        print("Card Number is :", str(UsercardNumber))
        print("Expiry date is :", str(ExpiryDate))
        print("Cvv Number is :", str(CVVnumber))
        print("Card Holder Name :", str(usr))
        print("Amount for paying :", str(AmountForPaying))
        print("method of payment is credit card")

        return redirect(url_for("paid"))
    else:
        return render_template('card1.html', post=str(usr), nxt=str(merchent))


@app.route("/Error/<usr>", methods = ["POST", "GET"])
def ErrorInMethodOfPayment(usr):
    return f"""<h1>ERROR , method of Payment is not given</h1>"""


@app.route("/finalPage", methods=["POST", "GET"])
def paid():
    return f""" <h1> payment is in progress..... </h1>"""
  
if __name__ == "__main__":
    app.run(debug=True)

