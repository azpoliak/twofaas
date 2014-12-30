from flask import Flask, request, jsonify
from flask import render_template
import random
import hashlib
from twilio.rest import TwilioRestClient
from pytwofaas import PyTwoFaas
import pymssql


account_sid = "AC2503925359b3b37abbeaaff6d87621f9"
auth_token = "44363a15bca971ddba81edd23cd56ee9"
twilio_num = "+18622775096"

# engine = pymssql.connect("201.212.8.208:9000", "twofass", "jagns", "twofass")
# cursor = engine.cursor()
# cursor.execute('select * from users')
# row = cursor.fetchone()
# while row:
#     print("ID=%d, Name=%s" % (row[0], row[2]))
#     row = cursor.fetchone()

# engine.close()

app = Flask(__name__)

def rand():
    x = hashlib.sha224(str(random.randint(0, 9999999))).hexdigest()
    return str(x[:6])

@app.route('/') 
def index():
    return 'Index!'

def sendsms(userPhNum, message):
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to=userPhNum, from_=twilio_num, 
    body="Your authentication key is " + message)
    return userPhNum

def sendToDB(compTK, userID, userNum, auth_key):
    return "auth_key: " + auth_key + "\n phone number: " + userNum 

def call(userPhNum):
    #need to get phone number and Company token and userID
    #phone number, company token will be received as json
    #parses the json and sends to database and user's phone

    client = TwilioRestClient(account_sid, auth_token)
    message = client.calls.create(to=userPhNum, from_=twilio_num, 
        url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")      


#this initializes the 2 factor process once company validates 1st auth 
@app.route('/init/<path>', methods=['POST', 'GET'])
def init():
    #need to get phone number and Company token and userID
    #phone number, company token will be received as json
    #parses the json and sends to database and user's phone
    #json = request.json
    #print(json)
    compTK = request.form['compTK']
    userID = request.form['userID']
    userNum = request.form['userNum']

    return path

   # auth_key = rand()
   # sendsms(userNum, auth_key)
    #call(userNum, auth_key)
    return sendToDB(compTK, userID, userNum, auth_key)
    #display 2nd fact input page

    #return jsonify(request)

@app.route('/validate', methods=['POST'])
def val():
    #gets the user id, phone number, and code and compares that to db
    userID = request.form['userID']
    userNum = request.form['userNum']
    print "userID: " + userID + "\n number: " + userNum
    return "userID: " + userID + "\n number: " + userNum


if __name__ == '__main__':
    app.debug = True
    app.run()
