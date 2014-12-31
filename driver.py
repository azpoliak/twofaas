from flask import Flask, request, jsonify
from flask import render_template
import random
import hashlib
from twilio.rest import TwilioRestClient
import pymssql
import sendgrid
import base64
from Crypto.Cipher import AES
from Crypto import Random
import json
from config import *
import os

unpad = lambda s : s[:-ord(s[len(s)-1:])]

class _AESCipher:

    def __init__( self, key ):
        self.key = key

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
twilio_num = TWILIO_NUMBER


app = Flask(__name__)

def rand():
    x = hashlib.sha224(str(random.randint(0, 9999999))).hexdigest()
    return str(x[:6])

@app.route('/') 
def index():
    return 'Welcome to the TwoFaas API! Two Factor Authentication in 2 minutes'
    #return app.send_static_url(demo/Extant/index.html)

def sendsms(userPhNum, message):
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to=userPhNum, from_=twilio_num, 
    body="Your authentication key is " + message)
    return userPhNum

def sendToDB(compTK, userID, userNum, auth_key):
    engine = pymssql.connect(DB_URL, DB_USER, DB_PASS, DB_NAME)
    engine.autocommit(True)
    cursor = engine.cursor()
    success = 0;
    q = "UPDATE Users SET Code='%s' WHERE CompanyId='%s' AND PhoneNum='%s' AND CompanyUserId='%s'" % (auth_key, compTK, userNum, userID)
    print q
    cursor.execute(q)
    print cursor.rowcount
    if cursor.rowcount == 0:
        ##insert query 
        query = "INSERT INTO Users (CompanyId, PhoneNum, Code, CompanyUserId) VALUES ('%s', '%s', '%s', '%s')" % (compTK, userNum, auth_key, userID)
        ##select query
        cursor.execute(query)
        success = cursor.rowcount
    else:
        success = cursor.rowcount;
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


def sendemail(user_add, auth_key):
    sg = sendgrid.SendGridClient(SENDGRID_USER, SENDGRID_PASS, raise_errors=True)

    body = "Your authentication key is " + auth_key + "."
    message = sendgrid.Mail(to=user_add, subject='Your Authentication Key', 
        text=body, from_email=SENDGRID_EMAIL)
    
    status, msg = sg.send(message)

    print status
    return status

def parseEncryption(publicKey, data):
    e = pymssql.connect(DB_URL, DB_USER, DB_PASS, DB_NAME)
    e.autocommit(True)
    c = e.cursor()
    ##insert query
    q = "SELECT KeyId FROM companies WHERE publickey='%s'" % (publicKey)
    ##select query
    c.execute(q)
    row = c.fetchone()
    if row is not None and row[0] is not None:
        privateKey = row[0]
        cipher = _AESCipher(privateKey)
        v =  cipher.decrypt(data)
        result = json.loads(v)
    else:
        result = False

    c.close()
    e.close()

    return result


#this initializes the 2 factor process once company validates 1st auth

@app.route('/init/<factor>', methods=['POST', 'GET'])
def init(factor=None):
    #need to get phone number and Company token and userID
    #phone number, company token will be received as json
    #parses the json and sends to database and user's phone

    publicKey = request.form['publicKey']
    data = request.form['data']

    response = parseEncryption(publicKey, data)

    if response is not False:
        compTK = response['compTK']
        userID = response['userID']
        if factor == "email":
            userNum = response['userEmail']
        else:
            userNum = response['userNum']

    auth_key = rand()
   
    success = sendToDB(compTK, userID, userNum, auth_key)

    if success is 1:
        if factor == "sms":
            sendsms(userNum, auth_key)
            return jsonify(success='true', message="Sent SMS to" + userNum)
        elif factor == "call":
            call(userNum)
            return jsonify(success='true', message="Sent Call to" + userNum)
        elif factor == "email":
            sendemail(userNum, auth_key)
            return jsonify(success='true', message="Sent Email to" + userNum)
    else:
        return jsonify(success='false', message="Failed to Second Second Factor")


@app.route('/validate', methods=['POST'])
def val():
    #gets the user id, phone number, and code and compares that to db
    publicKey = request.form['publicKey']
    data = request.form['data']
    response = parseEncryption(publicKey, data)

    if response is not False:
        userID = response['userID']
        compTK = response['compTK']
        inputCode = response['twoAuth']

    e = pymssql.connect(DB_URL, DB_USER, DB_PASS, DB_NAME)
    e.autocommit(True)
    c = e.cursor()
    ##insert query 
    q = "SELECT userid FROM users WHERE CompanyId='%s' AND CompanyUserId='%s' AND Code='%s'" % (compTK, userID, inputCode)
    ##select query
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

    if success:
        return jsonify(success='true')
    else:
        return jsonify(success='false')

@app.route('/valid', methods=['POST'])
def isValid():
    #gets the user id, phone number, and code and compares that to db
    publicKey = request.form['publicKey']
    data = request.form['data']
    response = parseEncryption(publicKey, data)

    if response is not False:
        userID = response['userID']
        compTK = response['compTK']

    e = pymssql.connect(DB_URL, DB_USER, DB_PASS, DB_NAME)
    e.autocommit(True)
    c = e.cursor()
    ##insert query 
    q = "SELECT keyid FROM users WHERE CompanyId='%s' AND CompanyUserId='%s'" % (compTK, userID)
    ##select query
    c.execute(q)
    row = c.fetchone()
    count = 0
    success = 0
    while row:
        if row is not None and row[0] is not None:
            success = 1
        count = count + 1
        row = c.fetchone()
    if count > 1:
        success = 0
        
    c.close()
    e.close()
    if success:
        return jsonify(success='true')
    else:
        return jsonify(success='false')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    #app.debug = True
    app.run(host='0.0.0.0', port=port)
