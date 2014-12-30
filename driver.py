from flask import Flask, request, jsonify
from flask import render_template
import random
import hashlib
from twilio.rest import TwilioRestClient
from pytwofaas import PyTwoFaas
import pymssql
import sendgrid

account_sid = "AC2503925359b3b37abbeaaff6d87621f9"
auth_token = "44363a15bca971ddba81edd23cd56ee9"
twilio_num = "+18622775096"


app = Flask(__name__)

def rand():
    x = hashlib.sha224(str(random.randint(0, 9999999))).hexdigest()
    return str(x[:6])

@app.route('/') 
def index():
    return 'Index!'

def sendsms(userPhNum, message):
    print "It gets here"
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to=userPhNum, from_=twilio_num, 
    body="Your authentication key is " + message)
    return userPhNum

def sendToDB(compTK, userID, userNum, auth_key):
    engine = pymssql.connect("201.212.8.208:9000", "twofass", "jagns", "twofass")
    engine.autocommit(True)
    cursor = engine.cursor()
    ##insert query 
    query = "INSERT INTO Users (CompanyId, PhoneNum, Code, CompanyUserId) VALUES ('%s', '%s', '%s', '%s')" % (compTK, userNum, auth_key, userID)
    ##select query
    cursor.execute(query)
    success = cursor.rowcount
    cursor.close()
    engine.close()

    return success
    

def call(userPhNum):
    #need to get phone number and Company token and userID
    #phone number, company token will be received as json
    #parses the json and sends to database and user's phone

    client = TwilioRestClient(account_sid, auth_token)
    message = client.calls.create(to=userPhNum, from_=twilio_num, 
        url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")


def send_email(user_add, auth_key):
    print "entered send_email"
    sg = sendgrid.SendGridClient('thepezman', 'israeltech', raise_errors=True)

    body = "Your authentication key is " + auth_key + "."
    message = sendgrid.Mail(to=user_add, subject='Your Authentication Key', 
        text=body, from_email='team@twofass.com')
    
    status, msg = sg.send(message)


#this initializes the 2 factor process once company validates 1st auth

@app.route('/init/<factor>', methods=['POST', 'GET'])
def init(factor=None):
    #need to get phone number and Company token and userID
    #phone number, company token will be received as json
    #parses the json and sends to database and user's phone
    #json = request.json
    #print(json)
    compTK = request.form['compTK']
    userID = request.form['userID']
    userNum = request.form['userNum']

    auth_key = rand()
   
    success = sendToDB(compTK, userID, userNum, auth_key)

    if success is 1:
        if factor == "sms":
            return sendsms(userNum, auth_key)
        elif factor == "call":
            return call(userNum)


@app.route('/validate', methods=['POST'])
def val():
    #gets the user id, phone number, and code and compares that to db
    userID = request.form['userID']
    userNum = request.form['userNum']
    inputCode = request.form['inputCode']
    print "userID: " + userID + "\n number: " + userNum
    return "userID: " + userID + "\n number: " + userNum


if __name__ == '__main__':
    app.debug = True
    app.run()
