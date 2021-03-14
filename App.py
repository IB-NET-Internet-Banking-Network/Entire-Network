"""
Author :- Manas Kumar mishra
Task :- Design a web app for login page
Begin DATE :- 05- MARCH-2021
"""
from flask import Flask, render_template, url_for, request, redirect



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

        if (str(methodOfPayment) == "Debit card"):
            return redirect(url_for("DebitCardPayment", usr=user))
        if (str(methodOfPayment) == "Credit card"):
            return redirect(url_for("CreditCardPayment", usr=user))
        else:
            return (redirect(url_for("ErrorInMethodOfPayment", usr=user)))
        # Take step based on the input in the form 
        # return render_template("form1.html")
        

        # for new page we can try
        # return redirect(url_for("user", usr= user))
    else:
        # For get method we will stay on the same page
        return (render_template('loginPage.html'))


@app.route("/Debitcard/<usr>", methods = ["POST", "GET"])
def DebitCardPayment(usr):
    return render_template('card1.html')


@app.route("/Creditcard/<usr>", methods = ["POST", "GET"])
def CreditCardPayment(usr):
    return render_template('card1.html')

@app.route("/Error/<usr>", methods = ["POST", "GET"])
def ErrorInMethodOfPayment(usr):
    return f"""<h1>ERROR , method of Payment is not given</h1>"""


if __name__ == "__main__":
    app.run(debug=True)

