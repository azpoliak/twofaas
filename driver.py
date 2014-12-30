from flask import Flask, request, jsonify
from flask import render_template
import random
import hashlib
from twilio.rest import TwilioRestClient
from pytwofaas import PyTwoFaas


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
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to="+972527482538", from_=twilio_num, 
    body="Your authentication key is " + message)
    return userPhNum

def sendToDB(compTK, userID, userNum, auth_key):
    return auth_key

def call(userPhNum):
    #need to get phone number and Company token and userID
    #phone number, company token will be received as json
    #parses the json and sends to database and user's phone

    client = TwilioRestClient(account_sid, auth_token)
    message = client.calls.create(to=userPhNum, from_=twilio_num, 
        url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")      

#this initializes the 2 factor process once company validates 1st auth 
@app.route('/init', methods=['POST', 'GET'])
def init():
    #need to get phone number and Company token and userID
    #phone number, company token will be received as json
    #parses the json and sends to database and user's phone
    #json = request.json
    #print(json)
    compTK = request.form['compTK']
    userID = request.form['userID']
    userNum = request.form['userNum']

    auth_key = rand()
    sendsms(userNum, auth_key)
    #call(userNum, auth_key)
    return sendToDB(compTK, userID, userNum, auth_key)
    #display 2nd fact input page

    #return jsonify(request)

@app.route('/admin')
def admin():
    return 'Admin'

@app.route('/firstlogInDone')
def auth():
    #gets phone number, and the auth token set my sys admin and sends code to user. 
    #write the user code, phone number, and user id to db 
    return 'Authorize'

@app.route('/validate')
def val():
    #gets the user id, phone number, and code and compares that to db
    return 'Validate'

@app.route('/login', methods=['POST', 'GET'])
def log_in():
    return app.send_static_file('login.html')

@app.route('/two_factor')
def two_factor():
    return app.send_static_file('twofac.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
