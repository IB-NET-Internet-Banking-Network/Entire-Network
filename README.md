
# Entire-Network
It contains, all nodes and important points for a Internet Banking Network system from user to bank.\
Team of IB-NET

 |Sno|Name | Roll number|
 |------|-------|-------|
 |1.| MANAS KUMAR MISHRA | ESD18I011  |
 |2.| KARTHIKA RAJESH | EDM18B026|
 |3.| GANESH T S| ESD18I006 |
 
## App.py

It is hosting full payment gateway, in that user can put their input for the payment gateway.
that page is looking like this.

![LOGIN_page](https://user-images.githubusercontent.com/47395502/110748206-64d63600-8265-11eb-90fc-1949e3383fbd.PNG)
 As of now we have three registered user
 |Sno|Name | Roll number|
 |------|-------|-------|
 |1.| MANAS | ESD18I011  |
 |2.| MISS KR | EDM18B026|
 |3.| GANESH | ESD18I006 |

 If we put any of this details in the login page as username and password respectively, then only we can go further.

## Template
This folder contains the all html files.

1. card1.html is for payment gateway pay now option.
2. loginpage.html is for user authentication.
3. otp.html is for otp check.
4. finalResult.html for showing final feedback. 


## static\CSS
It contains all css style files
1. style.css is for styling of login page.
2. card1.css is for styling of payment gateway. 

## Full working of the paymnet gateway
After putting the details in login page it will led us to a payment gateway page where we can enter the card details and amount.  We have filled the ganesh details then page was loking like this. Randomly it is choosing a merchent for paying.

![Paymentgateway_10](https://user-images.githubusercontent.com/47395502/111904535-7ee5f480-8a6d-11eb-9dab-790ea36f3176.PNG)

After that it will show the final authentication page (OTP) page. That will look like this.\
![OTP_page](https://user-images.githubusercontent.com/47395502/112095782-1ad54480-8bc3-11eb-8dcf-5625aef2ec36.PNG)

# Working\Simulation of this project
![paymentGateway](https://user-images.githubusercontent.com/47395502/112278781-30bd3500-8ca9-11eb-92f0-ead17afba5ad.gif)

![paymentGateway2](https://user-images.githubusercontent.com/47395502/112279831-58f96380-8caa-11eb-8607-58b99a1ab272.gif)

![paymentGateway3](https://user-images.githubusercontent.com/47395502/112280281-dc1ab980-8caa-11eb-9764-05dbfa46484d.gif)

## How to use it?
1. First start the App.py file.
2. Start the TPS_LAYER1.py.
3. Start the paymentProcessor.py.
4. Put 127.0.0.1:1000/payments into any browser. That will show login page.
5. Put MANAS as username and ESD18I011 as password. Then choose method of payment (this is very important).
6. After that it will show a payment gateway page. Put details as

|sno| Asked information | Registered information|
|---|-------------------|-----------------------|
|1.| Card number| 1001 0110 2002 0011|
|2.| Expirar date| 31-July-2023|
|3.| CVV| 000|
|4.|Card holder name| MANAS KUMAR MISHRA|
|5.|Amount| (Any amount)|

In each step, check the terminal of App.py. After that, there will be a page for OTP. Check the paymentProcessor.py terminal to put OTP. Put correct OTP.\
For other input, you may check the App.py for another register user details.


Thank you
