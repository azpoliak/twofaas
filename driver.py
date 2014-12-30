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
    compTK = request.form['compTK']
    inputCode = request.form['twoAuth']

    e = pymssql.connect("201.212.8.208:9000", "twofass", "jagns", "twofass")
    e.autocommit(True)
    c = e.cursor()
    ##insert query 
    q = "SELECT userid FROM users WHERE CompanyId='%s' AND CompanyUserId='%s' AND Code='%s'" % (compTK, userID, inputCode)
    ##select query
    print q
    c.execute(q)
    row = c.fetchone()
    count = 0;
    while row:
        count = count + 1;
        row = c.fetchone()
    success = 0;
    if count is 1:
        query = "update users set KeyId=NEWID() where CompanyId='%s' and CompanyUserId='%s' and Code='%s'" % (compTK, userID, inputCode)
        c.execute(query)
        success = c.rowcount
    c.close()
    e.close()

    return "COMPLETE"

@app.route('/valid', methods=['POST'])
def isValid():
    #gets the user id, phone number, and code and compares that to db
    userID = request.form['userID']
    compTK = request.form['compTK']

    e = pymssql.connect("201.212.8.208:9000", "twofass", "jagns", "twofass")
    e.autocommit(True)
    c = e.cursor()
    ##insert query 
    q = "SELECT keyid FROM users WHERE CompanyId='%s' AND CompanyUserId='%s'" % (compTK, userID)
    ##select query
    print q
    c.execute(q)
    row = c.fetchone()
    count = 0
    success = 0
    while row:
        if row is not None:
            success = 1
        count = count + 1
        row = c.fetchone()
    if count > 1:
        success = 0
        
    c.close()
    e.close()

    print success


if __name__ == '__main__':
    app.debug = True
    app.run()
